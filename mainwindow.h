#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QFile>
#include <QDebug>
#include <QVector>
#include <QCompleter>
#include <QRegExp>
#include "tleLineEdit.h"
//#include <QLineEdit>


#define LINE_EDIT_VIEW_LENGTH 15

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void readKnownGeoFile();
    void createLineEdits();

public slots:
    void nameCompleted(QString);
    void autoFillSatConstants(int);

private:
    QVector<tleLineEdit*> line1edits;
    QVector<tleLineEdit*> line2edits;
    QStringList knownGeoNames;
    QStringList knownGeoCatalogNumbers;
    QStringList knownGeoClassifications;
    QStringList knownGeoIntlDesignators;

    QCompleter *namecompleter;

    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
