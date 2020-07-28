#ifndef TLELINEEDIT_H
#define TLELINEEDIT_H

#include <QWidget>
#include <QLineEdit>
#include <QDebug>
#include <QKeyEvent>
#include <QVector>

class tleLineEdit : public QLineEdit
{
    Q_OBJECT
public:
    explicit tleLineEdit(const QString &contents, QWidget *parent = 0);

    void setIdx(int, int);
    void setVectorPtrs(QVector<tleLineEdit*>*, QVector<tleLineEdit*>*);
    void keyPressEvent(QKeyEvent *event);

private:
    int row;
    int col;
    QVector<tleLineEdit*> *v1;
    QVector<tleLineEdit*> *v2;
};

#endif // TLELINEEDIT_H
