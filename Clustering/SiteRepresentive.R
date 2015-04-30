SiteRepresentive <- function()
{
    FinRes <- data.frame()
    res <- data.frame()
    
    library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.0/Resources/library")
    m<-dbDriver("MySQL");
    con<-dbConnect(m,user='root',password='123456',host='localhost',dbname='Harrmann');
    
    NumSites <- dbGetQuery(con,"select distinct(site_id) from traces
                           where size_rcvd != 0 
                           and size_sent !=0 ")
    print(NumSites)
    for (i in NumSites[,1])
    {
        qString1 <- paste("select * from traces where site_id =",i,"and size_rcvd != 0 and size_sent !=0")
        res <- dbGetQuery(con,qString1)
        OrderedRes <-  res[order(res$pkts_rcvd,res$pkts_sent,decreasing = TRUE),]
        if(nrow(OrderedRes == 1))
        {
            FinRes <-rbind(FinRes,OrderedRes[1,])   
        }
        else
        {
            OrderedRes <- cbind(OrderedRes,lofactor(OrderedRes[4:9],k=nrow(OrderedRes)-1))
            FinRes <-rbind(FinRes,tail(OrderedRes[order(OrderedRes$outlier.scores,decreasing = T),],1))
        }
    }
    return(FinRes)
}