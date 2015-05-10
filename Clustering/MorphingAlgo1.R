MorphingAlgo <- function(a,b,d)
{
    res <- data.frame()
    o <- vector()
    j <- 1
    l <- 1
    SDI_NoM <- 0
    SDI_WiM  <- 0
    gbw <- 0
    for (i in 1:length(a))
    {
        if (i==1)
        {
            if (abs(a[i]) <= abs(b[l]))
            {
                o[j] <- b[l]
                j <- j+1
                l <- l+1
                print("i==1")
                print("###")
            }
            else
            {
                o[j] <- a[i]
                j <- j+1
                l <- l+1
            }
        }
        else if (a[i]==b[l])
        {
            o[j] <- b[l]
            j <- j+1
            l <- l+1
            print("equal")
            print("###")
        }
        else if (abs(a[i]) < abs(b[l]))
        {
            if (a[i] >= 0)
            {
                print("here")
                print(i)
                gbw <-( (b[l]-a[i]) / (max((a[1:i]),(b[1:l])) -min(abs(a[1:i]),abs(b[1:l])) ))
                print(gbw)
            }
            else
            {
                gbw <-( abs(b[l]-a[i]) / (max((-a[1:i]),(-b[1:l])) - min(abs(-a[1:i]),abs(-b[1:l]))) )
                print(gbw)
            }
            #
            o[j] <- a[i]
            #SDI_NoM <-  (( ( 2*sum(b[1:l] %in% o[1:j] ) ) ) / (length(b[1:l])+length(o[1:j]) ) )
            SDI_NoM <-  ( length(intersect(b[1:l],o[1:j])) / length(union(b[1:l],o[1:j]))  )
            print(SDI_NoM)
            #
            o[j] <- b[l]
            #SDI_WiM <-  (( ( 2*sum(b[1:l] %in% o[1:j] ) ) ) / (length(b[1:l])+length(o[1:j]) ) )
            SDI_WiM <-  ( length(intersect(b[1:l],o[1:j])) / length(union(b[1:l],o[1:j])) )
            SDI_WiM <- SDI_WiM-(1/d)*gbw
            print(SDI_WiM)
            #
            print("###")
            if (SDI_WiM < SDI_NoM)
            {
                o[j] <- a[i]
                j <- j+1
            }
            else
            {
                j <- j+1
            }
            l <- l+1
        }
        
        else if (abs(a[i]) > abs(b[l]))
        {
            o[j] <- a[i]
            #SDI_NoM <-  (( ( sum(b[1:l] %in% o[1:j] ) ) ) / (length(b[1:l])+length(o[1:j]) ) )
            SDI_NoM <-  ( length(intersect(b[1:l],o[1:j])) / length(union(b[1:l],o[1:j])) )
            #
            o[j] <- b[l]
            Rem <- abs(a[i]-(b[l]))
            j <- j+1
            l <- l+1
            while(Rem > 0)
            {
                o[j] <- b[l]
                Rem <- Rem-abs(b[l])
                j <- j+1
                l <- l+1
                print("loop")
                print(Rem)
                print(o)
            }
            k <- j-1
            if (a[i] >= 0)
            {
                gbw <- ( (sum(o[i:k])-a[i]) / ( max(o[1:k],a[1:i]) - min(abs(o[1:k]),abs(a[1:i])) ) )
                print(gbw)
            }
            else
            {
                gbw <- ( abs(sum(o[i:k])-a[i]) / ( max(-o[1:k],-a[1:i]) - min(abs(-o[1:k]),abs(-a[1:i])) ) )
                print(gbw)   
            }
            #SDI_WiM <-  (( ( sum(b[1:l] %in% o[1:k] ) ) )  / (length(b[1:l])+length(o[1:k]) ) )
            SDI_WiM <-  (( ( length(intersect(b[1:l],o[1:k])) ) )  / length(union(b[1:l],o[1:k])) )
            SDI_WiM <- SDI_WiM-( (1/d)*gbw )
            #
            print(SDI_NoM)
            print(SDI_WiM)
            #
            if (SDI_WiM < SDI_NoM )
            {
                print("final comparison")
                j<-i
                l<-i
                o[j] <- a[i]
                j <- j+1
                o[j]<-NA
                l<-l+1
            }
            print("###")
        }
    res <- rbind(res,c(i,j,l,SDI_NoM,gbw,SDI_WiM))    
    print(res)
    }
    return(o)
}