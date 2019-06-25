from gradient.commands import projects as projects_commands
from gradient.wizards import wizard
from gradient.wizards.wizard import get_application


def run_create_project_wizard():
    w = wizard.Wizard(projects_commands.CreateProjectCommand, u"Create new project")
    w.add_text_questions(("name", u"Name: "),
                         ("repoName", u"Repository name: "),
                         ("repoUrl", u"Repository URL: "),
                         ("api_key", u"apiKey: "), )

    root_container = w.get_layout()

    application = get_application(root_container)

    application.run()
