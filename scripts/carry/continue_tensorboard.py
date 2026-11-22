"""Read-only TensorBoard continuation: retained prefix + live resumed event files."""
import argparse
import json
from pathlib import Path
from tensorboard.backend.event_processing.event_file_loader import RawEventFileLoader
from tensorboard.compat.proto.event_pb2 import Event
from tensorboard.summary.writer.record_writer import RecordWriter


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True)
    p.add_argument('--cutoff',type=int,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();before=sorted(a.before.glob('events.out.tfevents.*'));after=sorted(a.after.glob('events.out.tfevents.*'))
    if not before or not after:raise ValueError('Both source runs must have event files')
    a.output.mkdir(parents=True,exist_ok=False);view=a.output/'stage1_continued';view.mkdir()
    target=view/'events.out.tfevents.0000000000.retained_checkpoint_prefix'
    retained=excluded=0;reward_steps=[]
    with target.open('wb') as stream:
        writer=RecordWriter(stream)
        for file in before:
            for raw in RawEventFileLoader(str(file)).Load():
                event=Event.FromString(raw)
                if event.step>a.cutoff:excluded+=1;continue
                writer.write(raw);retained+=1
                if any(v.tag=='Train/mean_reward' for v in event.summary.value):reward_steps.append(event.step)
        writer.flush()
    for file in after:(view/file.name).symlink_to(file.resolve())
    if not reward_steps or min(reward_steps)!=0 or max(reward_steps)!=a.cutoff:raise ValueError('Historical reward range does not match retained checkpoint')
    metadata=dict(scope='Visualization only; raw source logs unchanged',source_before=str(a.before.resolve()),source_after=str(a.after.resolve()),
        retained_through_step=a.cutoff,retained_event_records=retained,excluded_unsaved_event_records=excluded,
        historical_reward_steps=dict(first=min(reward_steps),last=max(reward_steps),count=len(reward_steps)),
        live_event_files=[str(p.resolve()) for p in after],run_name='stage1_continued',logdir=str(a.output.resolve()),
        display='Original steps0..cutoff plus live resumed stepscutoff+1 onward; no metric values recomputed')
    (a.output/'continuation_manifest.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps(metadata,indent=2))

if __name__=='__main__':main()
