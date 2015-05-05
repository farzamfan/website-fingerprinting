MBDDistance <- function()
{
    MBCCenters <- data.frame()
    FinalMBCDist <- data.frame(matrix(nrow=8))
    temp1 <- as.data.frame(table(FinTable$MBC9))
    for ( i in temp1[,1])
    {
        temp2 <- filter(FinTable,FinTable$MBC9 == i)
        MBCCenters <- rbind(MBCCenters,colMeans(temp2[,2:21]))
    }
    MBCCentersDist <- as.matrix(dist(MBCCenters))
    for (j in 1:nrow(MBCCentersDist))
    {
        print(head(order(MBCCentersDist[as.numeric(-j),as.numeric(j)]),nrow(MBCCentersDist-1))+1)
        FinalMBCDist <- cbind(FinalMBCDist,head(order(MBCCentersDist[as.numeric(-j),as.numeric(j)]),nrow(MBCCentersDist-1))+1)
    }
    FinalMBCDist <- FinalMBCDist[,-1]
    for (k in 1:9)
    {
        print(k)
        colnames(FinalMBCDist)[k] <- k
    }
}