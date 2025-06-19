import gradio

from gui.backend import (
    login, show_grades, show_schedule, show_stats,
    export_grades, export_schedule, export_stats,
    change_password, add_subject, add_team,
    add_student, add_student_team, add_grade,
    get_student_choices, get_subject_choices,
    get_team_choices, split_id,
)
from core import schedule

### === INTERFEJS GRADIO === ###
with gradio.Blocks() as block:
    gradio.Markdown("# Niezbędnik Studenta")
    with gradio.Tab("Logowanie", visible=True) as login_panel:
        login_input = gradio.Textbox(label="Login")
        password_input = gradio.Textbox(label="Hasło", type="password")
        login_button = gradio.Button("Zaloguj")
        status = gradio.Textbox(label="Status")
        student_id = gradio.State()
        student_name = gradio.State()

    with gradio.Tab("Panel Studenta", visible=False) as student_panel:
        with gradio.Tab("Oceny"):
            gradio.Markdown("## Oceny")
            grades_button = gradio.Button("Pokaz oceny")
            grades_out = gradio.Dataframe(headers=["Przedmiot", "Ocena", "Typ", "Semestr"])
            grades_button.click(fn=show_grades, inputs=[student_id], outputs=[grades_out])
            grades_export_btn = gradio.Button("Eksportuj oceny")
            grades_export_out = gradio.Textbox(label="Status")
            grades_export_btn.click(fn=export_grades, inputs=[student_id], outputs=[grades_export_out])

        with gradio.Tab("Plan zajec"):
            gradio.Markdown("## Plan zajęć")
            schedule_btn = gradio.Button("Pokaż plan")
            schedule_out = gradio.Dataframe(headers=["Dzień", "Przedmiot", "Od", "Do", "Sala", "Grupa"])
            schedule_btn.click(fn=show_schedule, inputs=student_id, outputs=schedule_out)
            schedule_export_btn = gradio.Button("Eksportuj plan zajęć")
            schedule_export_out = gradio.Textbox(label="Status")
            schedule_export_btn.click(fn=export_schedule, inputs=[student_id], outputs=[schedule_export_out])

        with gradio.Tab("Statystyki"):
            gradio.Markdown("## Statystyki")
            stats_btn = gradio.Button("Pokaż statystyki")
            stats_out = gradio.Dataframe(headers=["Semestr", "Średnia"])
            stats_btn.click(fn=show_stats, inputs=student_id, outputs=stats_out)
            stats_export_btn = gradio.Button("Eksportuj statystyki")
            stats_export_out = gradio.Textbox(label="Status")
            stats_export_btn.click(fn=export_stats, inputs=[student_id], outputs=[stats_export_out])

        with gradio.Tab("Ustawienia"):
            gradio.Markdown("## Ustawienia")
            gradio.Markdown("### Zmień hasło")
            old_password_input = gradio.Textbox(label="Stare hasło", type="password")
            new_password_input = gradio.Textbox(label="Nowe Hasło", type="password")
            repeat_new_password_input = gradio.Textbox(label="Powtórz nowe Hasło", type="password")
            setting_btn = gradio.Button("Zmień hasło")
            setting_out = gradio.Textbox(label="Status")
            setting_btn.click(fn=change_password, inputs=[student_id, old_password_input, new_password_input, repeat_new_password_input], outputs=[setting_out])

    with gradio.Tab("Panel Administratora", visible=False) as admin_panel:
        with gradio.Tab("Dodaj przedmiot"):
            gradio.Markdown("## Dodaj przedmiot")
            subject_name = gradio.Textbox(label="Nazwa przedmiotu")
            subject_btn = gradio.Button("Dodaj przedmiot")
            subject_out = gradio.Textbox(label="Status")

        with gradio.Tab("Dodaj zespół"):
            gradio.Markdown("## Dodaj zespół")
            team_name = gradio.Textbox(label="Nazwa zespołu")
            team_btn = gradio.Button("Dodaj zesół")
            team_out = gradio.Textbox(label="Status")

        with gradio.Tab("Dodaj studenta do zespołu"):
            gradio.Markdown("## Dodaj studenta do zespołu")
            with gradio.Row():
                student_dropdown_team = gradio.Dropdown(label="Student", choices=get_student_choices())
                team_dropdown = gradio.Dropdown(label="Zespół", choices=get_team_choices())
            student_team_btn = gradio.Button("Dodaj studenta do zespołu")
            student_team_out = gradio.Textbox(label="Status")

        with gradio.Tab("Dodaj ocene dla ucznia"):
            gradio.Markdown("## Dodaj ocene dla ucznia")
            with gradio.Row():
                student_dropdown_grade = gradio.Dropdown(label="Student", choices=get_student_choices())
                subject_dropdown = gradio.Dropdown(label="Przedmiot", choices=get_subject_choices())
            grade_in = gradio.Number(label="Ocena", minimum=2, maximum=5, value=5)
            grade_type = gradio.Dropdown(label="Typ", choices=["Practical Part", "Exam"])
            grade_semester = gradio.Number(label="Semester", minimum=1, maximum=8, value=1)
            grade_add_btn = gradio.Button("Dodaj ocenę")
            grade_admin_out = gradio.Textbox(label="Status")

        with gradio.Tab("Dodaj plan zajęć"):
            gradio.Markdown("## Dodaj plan zajęć")
            with gradio.Row():
                subject_dropdown_grade = gradio.Dropdown(label="Przedmiot", choices=get_subject_choices())
                team_dropdown_sc = gradio.Dropdown(label="Zespół", choices=get_team_choices())
                day_dropdown = gradio.Dropdown(
                    label="Dzień tygodnia",
                    choices=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                )
            start_time_input = gradio.Textbox(label="Godzina rozpoczęcia (HH:MM)", placeholder="np. 10:00")
            end_time_input = gradio.Textbox(label="Godzina zakończenia (HH:MM)", placeholder="np. 11:30")
            classroom_input = gradio.Textbox(label="Sala", placeholder="np. 203")
            add_schedule_btn = gradio.Button("Dodaj do planu")
            schedule_add_out = gradio.Textbox(label="Status")

        with gradio.Tab("Dodaj studenta"):
            gradio.Markdown("## Dodaj studenta")
            new_first_name_input = gradio.Textbox(label="Imię")
            new_last_name_input = gradio.Textbox(label="Nazwisko")
            new_login_input = gradio.Textbox(label="Login")
            new_password_input = gradio.Textbox(label="Hasło")
            new_user_button = gradio.Button("Utwórz konto ucznia")
            new_user_out = gradio.Textbox(label="Status")


        # --- Funkcje pomocniczne i clicki buttonow
        def admin_add_student_team_interface(student_label, team_label):
            return add_student_team(split_id(student_label), split_id(team_label))


        team_btn.click(fn=add_team, inputs=[team_name], outputs=[team_out, team_dropdown, team_dropdown_sc])
        student_team_btn.click(fn=admin_add_student_team_interface, inputs=[student_dropdown_team, team_dropdown], outputs=[student_team_out])
        new_user_button.click(fn=add_student, inputs=[new_first_name_input, new_last_name_input, new_login_input, new_password_input], outputs=[new_user_out, student_dropdown_team, student_dropdown_grade])

        def admin_add_schedule(subject_label, team_label, day, start, end, room):
            if (len(day) > 0 and len(start) > 0 and len(end) > 0):
                schedule.add_schedule(
                    split_id(subject_label),
                    split_id(team_label),
                    day, start, end, room)
                return "Plan zajęć dodany pozytywnie"
            return "Pola nie mogą być puste"


        add_schedule_btn.click(fn=admin_add_schedule, inputs=[
                subject_dropdown_grade,team_dropdown_sc,
                day_dropdown,start_time_input,
                end_time_input,classroom_input
            ],
            outputs=schedule_add_out)


        def admin_add_grade_interface(student_label, subject_label, grade, gtype, semester):
            return add_grade(split_id(student_label), split_id(subject_label), grade, gtype, semester)


        subject_btn.click(fn=add_subject, inputs=[subject_name], outputs=[subject_out, subject_dropdown])
        grade_add_btn.click(fn=admin_add_grade_interface, inputs=[student_dropdown_grade, subject_dropdown, grade_in, grade_type, grade_semester], outputs=[grade_admin_out])

    login_button.click(fn=login, inputs=[login_input, password_input], outputs=[status, student_id, student_name, student_panel, admin_panel, login_panel])

block.launch()