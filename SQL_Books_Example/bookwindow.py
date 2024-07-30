from PySide6.QtWidgets import (QAbstractItemView, QDataWidgetMapper,
                               QHeaderView, QMainWindow, QMessageBox, QApplication)
from PySide6.QtGui import QKeySequence
from PySide6.QtSql import QSqlRelation, QSqlRelationalTableModel, QSqlTableModel
from PySide6.QtCore import Qt, Slot
import createdb
from bookwindow import BookWindow
from bookdelegate import BookDelegate

class Book_window(QMainWindow, BookWindow): # A WINDOW TO SHOW THE BOKS AVAILABLE
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # INITIALIZE DB
        createdb.init_db()

        model= QSqlRelationalTableModel(self.bookTable)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.setTable("books")

        # REMEMBER THE INDEXES OF THE COLUMNS
        author_idx= model.fieldIndex("author")
        genre_idx= model.fieldIndex("genre")

        # SET THE RELATION TO THE OTEHR DATABASE COLUMS:
        model.setRelation(author_idx, QSqlRelation("authors", "id", "name"))
        model.setRelation(genre_idx, QSqlRelation("genres", "id", "name"))

        # SET THE LOCALIZED HEADER CAPTIONS:
        model.setHeaderData(author_idx, Qt.Horizontal, self.tr("Author Name"))
        model.setHeaderData(genre_idx, Qt.Horizontal, self.tr("Genre"))
        model.setHeaderData(model.fieldIndex("title"), Qt.Horizontal, self.tr("Title"))
        model.setHeaderData(model.fieldIndex("year"), Qt.Horizontal, self.tr("Year"))
        model.setHeaderData(model.fieldIndex("rating"), Qt.Horizontal, self.tr("Rating"))

        if not model.select(): print(model.lastError())

        # SET THE MODEL AND HIDE THE ID COLUMN:
        self.bookTable.setModel(model)
        self.bookTable.setItemDelegate(BookDelegate(self.bookTable))
        self.bookTable.setColumnHidden(model.fieldIndex("id"), True)
        self.bookTable.setSelectionMode(QAbstractItemView.SingleSelection)

        # INITIATE THE QUTHOR COMBO BOX:
        self.authorEdit.setModel(model.relationModel(author_idx))
        self.authorEdit.setModelColumn(model.relationModel(author_idx).fieldIndex("name"))

        self.genreEdit.setModel(model.relationModel(genre_idx))
        self.genreEdit.setModelColumn(model.relationModel(genre_idx).fieldIndex("name"))

        # LOCK AND PROHIBIT RESIZING OF THE WIDTH OF THE RATING COLUMN:
        self.bookTable.horizontalHeader().setSectionResizeMode(model.fieldIndex("rating"), QHeaderView.ResizeContents)

        mapper= QDataWidgetMapper(self)
        mapper.setModel(model)
        mapper.setItemDelegate(BookDelegate(self))
        mapper.addMapping(self.titleEdit, model.fieldIndex("title"))
        mapper.addMapping(self.yearEdit, model.fieldIndex("year"))
        mapper.addMapping(self.authorEdit, author_idx)
        mapper.addMapping(self.genreEdit, genre_idx)
        mapper.addMapping(self.ratingEdit, model.fieldIndex("rating"))

        selection_model= self.bookTable.selectionModel()
        selection_model.currnetRowChanged.connect(mapper.setCurrentModelIndex)

        self.bookTable.setCurrentIndex(model.index(0, 0))
        self.create_menubar()

    def showError(self, err):
        QMessageBox.critical(self, "Unable to initialize Database", f"Error initializing database: {err.text()}")

    def create_menubar(self):
        file_menu= self.menuBar().addMenu(self.tr("&File"))
        quit_action= file_menu.addAction(self.tr("&Quit"))
        quit_action.triggered.connect(QApplication.quit)

        help_menu= self.menuBar().addMenu(self.tr("&Help"))
        about_action= help_menu.addAction(self.tr("&About"))
        about_action.setShortcut(QKeySequence.HelpContents)
        about_action.triggered.connect(self.about)
        aboutQt_action= help_menu.addAction("&About Qt")
        aboutQt_action.triggered.connect(QApplication.aboutQt)

    @Slot()
    def about(self):
        QMessageBox.about(self, self.tr("About Books"), self.tr("<p>The <b>Books</b> example shows how to use QtSQL classes "
                                                                "with a model/view framework."))