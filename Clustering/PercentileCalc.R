BaseClusterFrame <- function()
{
    PacketCount <- data.frame(id=numeric(0),InCount=numeric(0),OutCount=numeric(0))
    
    library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.0/Resources/library")
    m<-dbDriver("MySQL");
    con<-dbConnect(m,user='root',password='123456',host='localhost',dbname='Harrmann');
    
    for (i in FinRes$id)
    {
        #incoming packet count
        qString3 <- paste("select count(*) from packets where trace_id=",i,"and size >0")
        InPackCount <- dbGetQuery(con,qString3)
        #print(InPackCount)
        #outgoing packet count
        qString4 <- paste("select count(*) from packets where trace_id=",i,"and size <0")
        OutPackCount <- dbGetQuery(con,qString4)
        #print(OutPackCount)
        PacketCount = rbind(PacketCount[,1:3],list(i,InPackCount,OutPackCount))
        
    }
    
    colnames(PacketCount) <- c("TraceID","InCount","OutCount")
    ClustTable <- data.frame(matrix(NA,ncol =25 ))
    
    for (i in FinRes$id)
    {
        k <- 2
        up <- 0
        down <- 0
        NextUp <- 0
        NextDown <- 0
        repeat
        {
            ClustTable[j,1] <- i
            NextUp <- up + ceiling(as.numeric(PacketCount[j,2])*0.1)
            qString2 <- paste("select avg(size) from (select size from packets where trace_id = ",i," and packets.size > 0 limit" ,up,",",NextUp," ) as subtable ")
            ClustTable[j,k] <- dbGetQuery(con,qString2)
            k <- k+2
            if (up > PacketCount[j,2])
            {
                break
            }
            up <- NextUp
        }
        k <- 3
        repeat
        {
            NextDown <- down + ceiling(as.numeric(PacketCount[j,3])*0.1)
            qString5 <- paste("select avg(size) from (select size from packets where trace_id = ",i," and packets.size < 0 limit" ,down,",",NextDown," ) as subtable ")
            ClustTable[j,k] <- dbGetQuery(con,qString5)
            k <- k+2
            if (down > PacketCount[j,3])
            {
                break
            }
            down <- NextDown
        }
        j <- j+1
    }
}