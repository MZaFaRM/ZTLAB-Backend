def get_formatted_attendance(subjects):
    for subject_key in subjects:
        subject = subjects[subject_key]
        subject["total_attendance"] = (
            int(round(((subject["present_classes"]) / subject["total_classes"]) * 100))
            if subject["total_classes"] > 0
            else 0
        )

        subject["duty_leave_percentage"] = (
            int(round((subject["duty_leaves"] / subject["total_classes"]) * 100))
            if subject["total_classes"] > 0
            else 0
        )
