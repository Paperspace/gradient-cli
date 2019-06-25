import collections

import six
from prompt_toolkit import Application
from prompt_toolkit.application import current
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import VSplit, HSplit, Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame, Label, TextArea, RadioList, Box, Button, HorizontalLine

from gradient import client, config, logger
from gradient.cli import common

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


class WizardLogger(logger.Logger):
    def __init__(self, output_field):
        self.output_field = output_field

    def _log(self, msg, *args, **kwargs):
        msg = unicode(msg)
        msg.strip()
        new_text = self.output_field.text + msg + u"\n"

        # Add text to output buffer.
        self.output_field.buffer.document = Document(
            text=new_text, cursor_position=len(new_text))


class Wizard(object):
    def __init__(self, command_cls, header):
        """

        :type command_cls: CommandBase
        :type header: unicode
        """
        self.command_cls = command_cls
        self.header = header
        self.questions = Questions()
        self._layout = None
        self._message_output_field = None
        self.logger = None

    def add_text_questions(self, *questions):
        """

        :type questions: tuple[str, unicode]
        """
        for field_name, question in questions:
            self.questions.add_text_question(field_name, question)

    def get_questions_widgets(self):
        question_widgets = [
            Frame(body=Label(text=unicode(self.header))),

        ]
        question_widgets += self.questions.get_widgets_list()

        create_button = Button(u"Create", handler=self.accept_create)
        exit_button = Button(u"Exit", handler=self.accept_exit)
        question_widgets.append(Box(VSplit([create_button, exit_button])))
        return question_widgets

    def get_layout(self):
        if self._layout is None:
            self._layout = self._get_layout()

        return self._layout

    def _get_layout(self):
        self.message_output_field = TextArea(style="class:output-field")

        layout = HSplit([HSplit(self.get_questions_widgets()),
                         HorizontalLine(),
                         self.message_output_field, ]
                        )
        self.logger = WizardLogger(self.message_output_field)

        return layout

    def accept_create(self):
        project = self.questions.get_json()
        api_key = project.pop("api_key", None)
        common.del_if_value_is_none(project)

        projects_api = client.API(config.CONFIG_HOST, api_key=api_key)

        command = self.command_cls(api=projects_api, logger_=self.logger)

        self.logger.debug("Executing command...")

        try:
            command.execute(project)
        except Exception as e:
            self.logger.error(str(e))

        self.logger.debug("Command executed...")

    def accept_exit(self):
        current.get_app().exit()


def get_application(root_container):
    style = Style.from_dict({
        u"background": u"blue",
    })

    application = Application(
        full_screen=True,
        layout=Layout(root_container, ),
        enable_page_navigation_bindings=True,
        key_bindings=bindings,
        style=style,
        mouse_support=True,
    )

    return application
