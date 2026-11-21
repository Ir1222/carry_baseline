"""Explicit policy gates: side friction grip must not be replaced by palm support."""


def tracking_suite_passed(groups,expected_scenarios,seeds):
    return bool(expected_scenarios and seeds>=10 and set(groups)==set(expected_scenarios)
        and all(g['success_rate']>=.8 for g in groups.values()))


def physical_failures(row):
    checks={
        'incomplete_episode':row['survived'],
        'contact_interruption':row['contact_continuity']>=.99,
        'hand_slip':row['max_hand_slip_m']<=.025,
        'box_ground_clearance':row['min_box_clearance_m']>=.03,
        'insufficient_friction_support':row['friction_weight_ratio_mean']>=.8,
        'non_lateral_contact':row['normal_vertical_fraction_max']<=.35,
        'contact_near_box_bottom':row['contact_height_above_bottom_min_m']>=.05,
        'nonhand_support':row['nonhand_box_contact_max_n']<=.5,
    }
    return [name for name,passed in checks.items() if not passed]
