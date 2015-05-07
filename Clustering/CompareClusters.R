CompareCluster <- function(ClustIndex1,ClustNumb1,ClustIndex2,ClustNumb2,range)
{
    library(dplyr)
    temp1 <- filter(FinTable,FinTable[,ClustIndex1]==ClustNumb1)
    temp2 <- filter(FinTable,FinTable[,ClustIndex2]==ClustNumb2)
    temp1 <- temp1[,1:21]
    temp2 <- temp2[,1:21]
    print(summary(temp1[,range]))
    print(summary(temp2[,range]))
}