#include "tleLineEdit.h"

tleLineEdit::tleLineEdit(const QString &contents, QWidget *parent):QLineEdit(parent)
{

}

void tleLineEdit::keyPressEvent(QKeyEvent *event){
    if(event->key() == Qt::Key_Up && row == 1){
        v1->at(col-1)->setFocus();
    }
    else if(event->key() == Qt::Key_Down && row == 0){
        v2->at(col-1)->setFocus();
    }
    else if(event->key() == Qt::Key_Left){
        if (row==0){
            v1->at(col-2)->setFocus();
        }
        else if (row==1){
            v2->at(col-2)->setFocus();
        }
    }
    else if(event->key() == Qt::Key_Right){
        if (row==0){
            v1->at(col)->setFocus();
        }
        else if (row==1){
            v2->at(col)->setFocus();
        }
    }
    else{
        // default handler for event
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
