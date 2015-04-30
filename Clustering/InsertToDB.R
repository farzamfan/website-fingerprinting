InsertToDB <- function()
{
	
	library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.0/Resources/library");
    m<-dbDriver("MySQL");
    con<-dbConnect(m,user='root',password='123456',host='localhost',dbname='Harrmann');
    dbWriteTable(con,"ClustTable",FinTable,append=F,overwrite=T,row.names=F)
}
