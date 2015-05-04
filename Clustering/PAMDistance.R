PamDistance <- function()
{
    for ( i in clValidPAM@clusterObjs$pam$'10'[2])
        {
            PAMCenters <- data.frame()
            PAMCentersDist <- data.frame()
            FinalPAMDist <- data.frame(matrix(nrow=nrow(PAMCentersDist)-1))
            print(i)
            print(FinTable[i,23])
            PAMCenters <- rbind(PAMCenters,FinTable[i,])
            PAMCentersDist <- dist(PAMCenters[,1:21])
        }
    for (j in 1:nrow(PAMCentersDist))
        {
            print(head(order(PAMCentersDist[as.numeric(-j),as.numeric(j)]),nrow(PAMCentersDist-1))+1)
            FinalPAMDist <- cbind(FinalPAMDist,head(order(PAMCentersDist[as.numeric(-j),as.numeric(j)]),nrow(PAMCentersDist-1))+1)
        }
    FinalPAMDist <- FinalPAMDist[,-1]
    k <- clValidPAM@clusterObjs$pam$'10'[2]    
    for(l in 1:length(FinalPAMDist))
        {
            colnames(FinalPAMDist)[l] <- k$id.med[l]
        }
    return(FinalPAMDist)    
}