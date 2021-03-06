IndexCalc <- function(Index)
{
    indices <- data.frame()
    temp <- data.frame()
    library(clusterCrit);
    #needs clusterVectors
    for(i in 1:9)
    {
        k<-1
        while(k < (length(Index)+1) )
        {
            temp <- c(intCriteria(as.matrix(mydata[,2:21]),as.integer(ClusterVectors[,i]),Index),as.character(colnames(ClusterVectors[i])))
            #print(temp)
            indices[i,k] <- temp[k]
            indices[i,k+1] <- temp[k+1]
            #print(indices)
            k <- k+1
        }
    }
    indices <- rbind(indices,c("max","max","max","min","min","-"))
    return(as.data.frame(indices))
    
    #return(as.matrix(indices))
    #print(indices[with(indices[-10,],order(indices$calinski_harabasz,indices$dunn,indices$silhouette,-as.numeric(indices$davies_bouldin))),])
}