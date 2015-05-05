SOMDistance <- function()
{
    SOMCenters <- data.frame()
    FinalSOMDist <- data.frame(matrix(nrow=9))
    temp1 <- as.data.frame(table(FinTable$SOM10))
    for ( i in temp1[,1])
    {
        temp2 <- filter(FinTable,FinTable$SOM10 == i)
        SOMCenters <- rbind(SOMCenters,colMeans(temp2[,2:21]))
    }
    SOMCentersDist <- as.matrix(dist(SOMCenters))
    for (j in 1:nrow(SOMCentersDist))
    {
        print(head(order(SOMCentersDist[as.numeric(-j),as.numeric(j)]),nrow(SOMCentersDist-1))+1)
        FinalSOMDist <- cbind(FinalSOMDist,head(order(SOMCentersDist[as.numeric(-j),as.numeric(j)]),nrow(SOMCentersDist-1))+1)
    }
    FinalSOMDist <- FinalSOMDist[,-1]
    for (k in 1:10)
    {
        print(k)
        colnames(FinalSOMDist)[k] <- k
    }
}