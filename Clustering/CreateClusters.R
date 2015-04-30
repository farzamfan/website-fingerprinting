CreateClusters <- function()
{

    t1 <- Sys.Date()
    clValidModelBased <- clValid(mydata[,2:21],nClust=8:10,clMethods = "model",validation = c("internal","stability"),maxitems = 11000,neighbSize = length(mydata)-1)
    t2 <- Sys.Date()
    clValidPAM <- clValid(mydata[,2:21],nClust=8:10,clMethods = "pam",validation = c("internal","stability"),maxitems = 11000,neighbSize = length(mydata)-1)
    t3 <- Sys.Date()
    clValidSOM <- clValid(mydata[,2:21],nClust=8:10,clMethods = "som",validation = c("internal","stability"),maxitems = 11000,neighbSize = length(mydata)-1)
}