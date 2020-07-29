#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // read the known geo file
    readKnownGeoFile();

    // initialise line edits for each character
    createLineEdits();

    // initialise completer for name
    namecompleter = new QCompleter(knownGeoNames, this);
    namecompleter->setCaseSensitivity(Qt::CaseInsensitive);
    ui->satnameEdit->setCompleter(namecompleter);
    connect(namecompleter, SIGNAL(activated(QString)), this, SLOT(nameCompleted(QString)));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::readKnownGeoFile(){
    QString fileName = "knownGeos.txt";
    QFile inputFile(fileName);
    if (inputFile.open(QIODevice::ReadOnly))
    {
        QTextStream in(&inputFile);
        while (!in.atEnd())
        {
          QString line = in.readLine();
          QStringList elements = line.split(',');

          knownGeoNames.push_back(elements.at(0));
          knownGeoCatalogNumbers.push_back(elements.at(1));
          knownGeoClassifications.push_back(elements.at(2));
          knownGeoIntlDesignators.push_back(elements.at(3));

        }
        inputFile.close();
    }
}

void MainWindow::createLineEdits(){
    // first make all the line edits
    for (int i = 0; i < 69; i++){
        tleLineEdit *edit = new tleLineEdit("");
        edit->setIdx(0, i+1);
        edit->setVectorPtrs(&line1edits, &line2edits);

        edit->setMaxLength(1); // set the input length
        edit->setMaximumWidth(LINE_EDIT_VIEW_LENGTH); // set the view length
        line1edits.push_back(edit);
        ui->gridLayout->addWidget(edit, 0, i + 1);

        tleLineEdit *edit2 = new tleLineEdit("");
        edit2->setIdx(1, i+1);
        edit2->setVectorPtrs(&line1edits, &line2edits);

        edit2->setMaxLength(1); // set the input length
        edit2->setMaximumWidth(LINE_EDIT_VIEW_LENGTH); // set the view length
        line2edits.push_back(edit2);
        ui->gridLayout->addWidget(edit2, 1, i + 1);
    }

    // adjust grid layout spacing to make it look cleaner
    ui->gridLayout->setHorizontalSpacing(1);

    // first two of each row can be set and then disabled
    line1edits.at(0)->setText("1");
    line2edits.at(0)->setText("2");

    line1edits.at(0)->setEnabled(false);
    line1edits.at(1)->setEnabled(false);
    line2edits.at(0)->setEnabled(false);
    line2edits.at(1)->setEnabled(false);

}

void MainWindow::autoFillSatConstants(int idx){
    // set catalog number
    for (int i = 2; i < 7; i++){
        line1edits.at(i)->setText(knownGeoCatalogNumbers.at(idx)[i-2]);
        line2edits.at(i)->setText(knownGeoCatalogNumbers.at(idx)[i-2]);
    }

    // set classification
    line1edits.at(7)->setText(knownGeoClassifications.at(idx));

    // set international designators
    for (int i = 9; i < 17; i++){
        line1edits.at(i)->setText(knownGeoIntlDesignators.at(idx)[i-9]);
    }
}

void MainWindow::nameCompleted(QString name){
    QRegExp rx(name);
    int idx = knownGeoNames.indexOf(rx);

    autoFillSatConstants(idx);

    qDebug()<<knownGeoCatalogNumbers.at(idx);
    qDebug()<<knownGeoClassifications.at(idx);
    qDebug()<<knownGeoIntlDesignators.at(idx);
}

void MainWindow::calculateCheckSum(){
    uint32_t checksum = 0;

    char c;
    QString s;
    int d;

    for (int i = 0; i < line1edits.size(); i++){
        s = line1edits.at(i)->text();
        if (s.size() > 0){ // only process if there's a character
            c = s.at(0).toLatin1();
            if (isdigit(c)){ // if it's a digit then output the digit
                d = atoi(&c);
                qDebug() << d;
            }
            else if (c == '.'){
                d = 1;
            }

            checksum = checksum + d;
        }
    }

    // repeat it for line 2, without the final one
    for (int i = 0; i < line2edits.size() - 1; i++){
        s = line2edits.at(i)->text();
        if (s.size() > 0){ // only process if there's a character
            c = s.at(0).toLatin1();
            if (isdigit(c)){ // if it's a digit then output the digit
                d = atoi(&c);
                qDebug() << d;
            }
            else if (c == '.'){
                d = 1;
            }

            checksum = checksum + d;
        }
    }

    qDebug() << checksum;
}


void MainWindow::on_addTLEbtn_clicked()
{
    // verify the checksum
    calculateCheckSum();
}
