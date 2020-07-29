#include "tleLineEdit.h"

tleLineEdit::tleLineEdit(const QString &contents, QWidget *parent):QLineEdit(parent)
{
    connect(this, SIGNAL(textEdited(QString)), this, SLOT(moveWhenFilled()));
}

bool tleLineEdit::event(QEvent *e){
    if (e->type() == QEvent::KeyPress){
        QKeyEvent *ke = (QKeyEvent*)e;
        qDebug() << "in event override";
        if (ke->key() == Qt::Key_Tab){
            qDebug()<< "reached here";
            moveRight();
        }
        else{
            return QLineEdit::event(e);
        }
    }
    else{
        return QLineEdit::event(e);
    }

//    return QLineEdit::event(e);
}

void tleLineEdit::keyPressEvent(QKeyEvent *event){
    if(event->key() == Qt::Key_Up && row == 1){
        moveUp();
    }
    else if(event->key() == Qt::Key_Down && row == 0){
        moveDown();
    }
    else if(event->key() == Qt::Key_Left){
        moveLeft();
    }
    else if(event->key() == Qt::Key_Right){
        moveRight();
    }
//    else if(event->key() == Qt::Key_Tab && col < v1->size()){
//        qDebug() << "special tab handler";
//        moveRight();
//    }
    else if(event->key() == Qt::Key_Backspace && text().size() == 0){
        moveLeft();
    }
    else{
        // default handler for event
        qDebug()<<"default handler";
//        qDebug()<<event->key();
        qDebug()<< row << col << "\n";
        QLineEdit::keyPressEvent(event);
    }
}

void tleLineEdit::setIdx(int in_row, int in_col){
    row = in_row;
    col = in_col;
}

void tleLineEdit::setVectorPtrs(QVector<tleLineEdit*> *in_v1, QVector<tleLineEdit*> *in_v2){
    v1 = in_v1;
    v2 = in_v2;
}

void tleLineEdit::moveWhenFilled(){
    if (text().size() == 1){
        moveRight();
    }
}

void tleLineEdit::moveRight(){
    this->clearFocus();
    if (row==0 && col < v1->size()){
        v1->at(col)->setFocus();
    }
    else if (row==1 && col < v1->size()){
        v2->at(col)->setFocus();
    }
}

void tleLineEdit::moveLeft(){
    this->clearFocus();
    if (row==0){
        v1->at(col-2)->setFocus();
    }
    else if (row==1){
        v2->at(col-2)->setFocus();
    }
}

void tleLineEdit::moveUp(){
    this->clearFocus();
    v1->at(col-1)->setFocus();
}

void tleLineEdit::moveDown(){
    this->clearFocus();
    v2->at(col-1)->setFocus();
}
