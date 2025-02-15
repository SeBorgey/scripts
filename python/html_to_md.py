import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QStatusBar
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re

class HtmlToMarkdownLatexConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML to Markdown+LaTeX Converter")
        self.setGeometry(100, 100, 1200, 700)  # Увеличен размер окна для размещения статусной строки

        self.init_ui()

    def init_ui(self):
        # Центральный виджет и основной вертикальный слой
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Верхний слой: кнопки
        button_layout = QHBoxLayout()

        # Настройка шрифта для кнопок
        button_font = QFont()
        button_font.setPointSize(12)  # Увеличение размера шрифта

        # Кнопка "Вставить"
        self.paste_button = QPushButton("Вставить")
        self.paste_button.setFixedHeight(50)  # Увеличение высоты кнопки
        self.paste_button.setFont(button_font)
        self.paste_button.clicked.connect(self.paste_html)

        # Кнопка "Конвертировать"
        self.convert_button = QPushButton("Конвертировать (last_exam)")
        self.convert_button.setFixedHeight(50)  # Увеличение высоты кнопки
        self.convert_button.setFont(button_font)
        self.convert_button.clicked.connect(self.convert_text)

        self.convert_proof_button = QPushButton("Конвертировать (hugginface)")
        self.convert_proof_button.setFixedHeight(50)  # Увеличение высоты кнопки
        self.convert_proof_button.setFont(button_font)
        self.convert_proof_button.clicked.connect(self.convert_proof_text)

        # Кнопка "Копировать"
        self.copy_button = QPushButton("Копировать")
        self.copy_button.setFixedHeight(50)  # Увеличение высоты кнопки
        self.copy_button.setFont(button_font)
        self.copy_button.clicked.connect(self.copy_result)

        # Добавление кнопок в верхний слой с отступами
        button_layout.addWidget(self.paste_button)
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.convert_proof_button)
        button_layout.addWidget(self.copy_button)

        # Добавление верхнего слоя в главный слой
        main_layout.addLayout(button_layout)

        # Нижний слой: два текстовых поля
        text_layout = QHBoxLayout()

        # Левая сторона: Ввод HTML
        left_layout = QVBoxLayout()
        left_label = QLabel("HTML Input:")
        left_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.html_input = QTextEdit()
        self.html_input.setPlaceholderText("Вставьте ваш HTML здесь...")
        left_layout.addWidget(left_label)
        left_layout.addWidget(self.html_input)

        # Правая сторона: Вывод результата
        right_layout = QVBoxLayout()
        right_label = QLabel("Result (.md with LaTeX):")
        right_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setPlaceholderText("Здесь будет отображен результат...")
        right_layout.addWidget(right_label)
        right_layout.addWidget(self.result_output)

        # Добавление левой и правой стороны в нижний слой
        text_layout.addLayout(left_layout)
        text_layout.addLayout(right_layout)

        # Добавление нижнего слоя в главный слой
        main_layout.addLayout(text_layout)

        # Установка главного слоя в центральный виджет
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Создание статусной строки
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def paste_html(self):
        """
        Вставляет текст из буфера обмена в левое текстовое поле.
        """
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            self.html_input.setPlainText(text)
            self.status_bar.showMessage("Текст успешно вставлен из буфера обмена.", 5000)  # Сообщение отображается 5 секунд
        else:
            self.status_bar.showMessage("Буфер обмена пуст.", 5000)

    def copy_result(self):
        """
        Копирует текст из правого текстового поля в буфер обмена.
        """
        text = self.result_output.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.status_bar.showMessage("Результат скопирован в буфер обмена.", 5000)
        else:
            self.status_bar.showMessage("Нет текста для копирования.", 5000)

    def convert_text(self):
        """
        Конвертирует HTML из левого текстового поля в Markdown+LaTeX и выводит результат.
        Исправляет избыточные слеши и предотвращает дублирование формул.
        """
        html_text = self.html_input.toPlainText()
        if not html_text.strip():
            self.status_bar.showMessage("Вставьте HTML текст для конвертации.", 5000)
            return

        try:
            # Парсинг HTML с помощью BeautifulSoup
            soup = BeautifulSoup(html_text, 'html.parser')

            # Поиск всех <span data-testid="react-katex"> элементов
            for katex_span in soup.find_all('span', attrs={'data-testid': 'react-katex'}):
                # Поиск вложенного <annotation encoding="application/x-tex">
                annotation = katex_span.find('annotation', attrs={'encoding': 'application/x-tex'})
                if annotation:
                    latex_code = annotation.get_text().strip()

                    # Определение, должна ли формула быть инлайновой или блочной
                    # Для простоты предполагаем, что все формулы инлайновые
                    # Можно расширить логику при необходимости
                    latex_markdown = f"${latex_code}$"

                    # Замена всего <span data-testid="react-katex"> на LaTeX-код
                    katex_span.replace_with(latex_markdown)

            # Преобразование обработанного HTML в Markdown
            markdown = md(str(soup), heading_style="ATX")

            # Дополнительная очистка: удаление лишних переносов строк
            markdown = re.sub(r'\n{3,}', '\n\n', markdown)

            # Удаление обратных слешей перед спецсимволами, если они были добавлены
            # Это может потребоваться, если markdownify экранирует некоторые символы
            markdown = markdown.replace('\\{', '{').replace('\\}', '}').replace('\\(', '(').replace(
                '\\)', ')')

            # Удаление лишних обратных слешей перед командами LaTeX
            # Например, заменяем '\\rightarrow' на '\rightarrow'
            markdown = re.sub(r'\\(\\[a-zA-Z]+)', r'\1', markdown)

            markdown = re.sub(r'\\([=*._|])', r'\1', markdown)

            # Установка результата в правое текстовое поле
            self.result_output.setPlainText(markdown)

            # Обновление статусной строки
            self.status_bar.showMessage("Конвертация выполнена успешно.", 5000)
        except Exception as e:
            # Обработка ошибок и обновление статусной строки
            self.status_bar.showMessage(f"Ошибка при конвертации: {str(e)}", 5000)

    def convert_proof_text(self):
        """
        Конвертирует HTML доказательств из левого текстового поля в Markdown+LaTeX и выводит результат.
        Исправляет избыточные слеши и предотвращает дублирование формул.
        """
        html_text = self.html_input.toPlainText()
        if not html_text.strip():
            self.status_bar.showMessage("Вставьте HTML текст для конвертации.", 5000)
            return

        try:
            # Парсинг HTML с помощью BeautifulSoup
            soup = BeautifulSoup(html_text, 'html.parser')

            # Обработка всех формул: как блочных, так и инлайновых
            for katex_span in soup.find_all('span', class_=re.compile('katex')):
                # Определение, является ли формула блочной
                is_display = 'katex-display' in katex_span.get('class', [])

                # Поиск вложенного <annotation encoding="application/x-tex">
                annotation = katex_span.find('annotation', attrs={'encoding': 'application/x-tex'})
                if annotation:
                    latex_code = annotation.get_text().strip()

                    # Определение, должна ли формула быть инлайновой или блочной
                    # Если формула находится внутри абзаца (<p>), считаем её инлайновой
                    parent = katex_span.find_parent(
                        ['p', 'li', 'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    if parent and parent.name in ['p', 'li', 'span']:
                        # Инлайновая формула
                        latex_markdown = f"${latex_code}$"
                    else:
                        # Блочная формула
                        latex_markdown = f"$$\n{latex_code}\n$$"

                    # Замена всего <span class="katex"> или <span class="katex-display"> на LaTeX-код
                    katex_span.replace_with(latex_markdown)

            # Преобразование обработанного HTML в Markdown
            markdown = md(str(soup), heading_style="ATX")

            # Дополнительная очистка: удаление лишних переносов строк
            markdown = re.sub(r'\n{3,}', '\n\n', markdown)

            # Удаление обратных слешей перед спецсимволами, если они были добавлены
            # Это может потребоваться, если markdownify экранирует некоторые символы
            markdown = markdown.replace('\\{', '{').replace('\\}', '}').replace('\\(', '(').replace(
                '\\)', ')')

            # Удаление лишних обратных слешей перед командами LaTeX
            # Например, заменяем '\\rightarrow' на '\rightarrow'
            markdown = re.sub(r'\\(\\[a-zA-Z]+)', r'\1', markdown)

            # Удаление обратных слешей перед определенными символами: '=', '*', '.', '_', '|'
            markdown = re.sub(r'\\([=*._|])', r'\1', markdown)

            # Удаление обратных слешей перед математическими операторами, если они еще остались
            # Добавьте дополнительные символы по необходимости
            markdown = re.sub(r'\\([+\-*/^<>&\[])', r'\1', markdown)

            # Удаление лишних обратных слешей, оставшихся перед пробелами или другими символами
            markdown = re.sub(r'\\\s', ' ', markdown)

            # Установка результата в правое текстовое поле
            self.result_output.setPlainText(markdown)

            # Обновление статусной строки
            self.status_bar.showMessage("Конвертация  выполнена успешно.", 5000)
        except Exception as e:
            # Обработка ошибок и обновление статусной строки
            self.status_bar.showMessage(f"Ошибка при конвертации: {str(e)}", 5000)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HtmlToMarkdownLatexConverter()
    window.show()
    sys.exit(app.exec_())
