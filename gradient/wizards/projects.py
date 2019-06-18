import collections

import six
from prompt_toolkit import Application
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import Layout, VSplit, HSplit, FloatContainer, Float
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame, Label, TextArea, RadioList, Box, Button, Dialog

from gradient import client, config
from gradient.cli import common
from gradient.commands import projects as projects_commands

if not six.PY2:
    unicode = str

bindings = KeyBindings()
bindings.add(u'tab')(focus_next)
bindings.add(u"right")(focus_next)
bindings.add(u'enter')(focus_next)
bindings.add(u"left")(focus_previous)
bindings.add(u's-tab')(focus_previous)


@bindings.add(u"c-c")
def _(event):
    event.app.exit()


@bindings.add('c-space')
def _(event):
    " Initialize autocompletion, or select the next completion. "
    buff = event.app.current_buffer
    if buff.complete_state:
        buff.complete_next()
    else:
        buff.start_completion(select_first=False)


default_question_style = u"green"


class Question(object):
    def __init__(self, question):
        self.question = question
        self.question_widget = self._get_question_widget()
        self.answer_widget = self._get_answer_widget()
        self.widget = self._get_widget()

    @property
    def answer(self):
        return self.answer_widget.text

    def _get_question_widget(self):
        return Label(
            self.question,
            # style=self.style,
        )

    def _get_answer_widget(self):
        return TextArea(multiline=False)

    def _get_widget(self):
        return Frame(
            VSplit(
                [
                    self.question_widget,
                    self.answer_widget,
                ],
            ),
        )


class RadioQuestion(Question):
    def __init__(self, question, answers):
        self.answers = answers
        super(RadioQuestion, self).__init__(question)

    @property
    def answer(self):
        return self.answer_widget.current_value

    def _get_answer_widget(self):
        return RadioList(self.answers)


class Questions(object):
    def __init__(self):
        self._questions = collections.OrderedDict()

    def add_text_question(self, field_name, question):
        q = Question(question)
        self._questions[field_name] = q

    def add_radio_question(self, field_name, question, answers):
        q = RadioQuestion(question, answers)
        self._questions[field_name] = q

    def get_widgets_list(self):
        return [question.widget for question in self._questions.values()]

    def get_json(self):
        return {field_name: question.answer
                for field_name, question in self._questions.items()}


questions = Questions()
questions.add_text_question("name", u"Name: ")
questions.add_text_question("repoName", u"Repository name: ")
questions.add_text_question("repoUrl", u"Repository URL: ")
questions.add_text_question("api_key", u"apiKey: ")

style = Style.from_dict({
    u"background": u"blue",
})


class DialogLogger(object):
    def log(self, msg):
        layout = get_app().layout
        dialog = Dialog(body=Label(text=msg))
        layout.container.floats.append(
            Float(content=dialog)
        )

    def log_error_response(self, data):
        error_str = data.get("error")
        details = data.get("details")
        message = data.get("message")

        if not any((error_str, details, message)):
            raise ValueError("No error messages found")

        if error_str:
            try:
                self.error(error_str["message"])
            except (KeyError, TypeError):
                self.error(str(error_str))

        if details:
            if isinstance(details, dict):
                for key, val in details.items():
                    if isinstance(val, six.string_types):
                        val = [val]

                    for v in val:
                        msg = "{}: {}".format(key, str(v))
                        self.error(msg)
            else:
                self.error(details)

        if message:
            self.error(str(message))


def accept_create():
    project = questions.get_json()
    api_key = project.pop("api_key", None)
    common.del_if_value_is_none(project)

    projects_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = projects_commands.CreateProjectCommand(api=projects_api, logger_=DialogLogger())
    command.execute(project)
    get_app().exit()


def accept_exit():
    get_app().exit()


create_button = Button(u"Create", handler=accept_create)
exit_button = Button(u"Exit", handler=accept_exit)

question_widgets = [
    Frame(body=Label(text=u"Create new job")),

]
question_widgets += questions.get_widgets_list()
question_widgets.append(Box(VSplit([create_button, exit_button])))

# float_container =
# root_container = HSplit(
#     question_widgets,
#     # style=u"grey",
# )


root_container = FloatContainer(HSplit(question_widgets), [])

application = Application(
    full_screen=True,
    layout=Layout(root_container, ),
    enable_page_navigation_bindings=True,
    key_bindings=bindings,
    style=style,
    mouse_support=True,
)

if __name__ == '__main__':
    application.run()
