MorphingAlgo <- function(a,b,d,treshold)
{
    res <- data.frame(matrix(ncol=6))
    colnames(res) <- c("i","j","l","SDI_NoM","gbw","SDI_WiM")
    o <- vector()
    j <- 1
    l <- 1
    i <- 1
    SDI_NoM <- 0
    SDI_WiM  <- 0
    gbw <- 0
    while (i <= length(a))
    {
        while (is.na(b[l]) || sign(b[l]) != sign(a[i]))
        {
            print("b is finished in beginning")
            l <- l-1
        }
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
            cat("a[",i,"] < b[",l,"] -> ",a[i],b[l],"\n")
            if (a[i] >= 0)
            {
                gbw <-( (b[l]-a[i]) / (max((a[1:i]),(b[1:l])) -min(abs(a[1:i]),abs(b[1:l])) ))
            }
            else
            {
                gbw <-( abs(b[l]-a[i]) / (max((-a[1:i]),(-b[1:l])) - min(abs(-a[1:i]),abs(-b[1:l]))) )
            }
            #
            o[j] <- a[i]
            #SDI_NoM <-  (( ( 2*sum(b[1:l] %in% o[1:j] ) ) ) / (length(b[1:l])+length(o[1:j]) ) )
            SDI_NoM <-  ( length(intersect(b[1:l],o[1:j])) / length(union(b[1:l],o[1:j]))  )
            #
            o[j] <- b[l]
            #SDI_WiM <-  (( ( 2*sum(b[1:l] %in% o[1:j] ) ) ) / (length(b[1:l])+length(o[1:j]) ) )
            SDI_WiM <-  ( length(intersect(b[1:l],o[1:j])) / length(union(b[1:l],o[1:j])) )
            SDI_WiM <- SDI_WiM-(1/d)*gbw
            #
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
            print("###")
        }
        
        else if (abs(a[i]) > abs(b[l]))
        {
            cat("a[",i,"] > b[",l,"] -> ",a[i],b[l],"\n")
            org <- j
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
                if (is.na(b[l]) || sign(b[l]) != sign(a[i]))
                {
                    print("b is finished before loop")
                    l <- l-1
                }
                print("loop")
                o[j] <- b[l]
                Rem <- Rem-abs(b[l])
                j <- j+1
                l <- l+1
            }
            k <- j-1
            if (a[i] >= 0)
            {
                gbw <- ( (sum(o[i:k])-a[i]) / ( max(o[1:k],a[1:i]) - min(abs(o[1:k]),abs(a[1:i])) ) )
            }
            else
            {
                gbw <- ( abs(sum(o[i:k])-a[i]) / ( max(-o[1:k],-a[1:i]) - min(abs(-o[1:k]),abs(-a[1:i])) ) )   
            }
            #SDI_WiM <-  (( ( sum(b[1:l] %in% o[1:k] ) ) )  / (length(b[1:l])+length(o[1:k]) ) )
            SDI_WiM <-  (( ( length(intersect(b[1:l],o[1:k])) ) )  / length(union(b[1:l],o[1:k])) )
            SDI_WiM <- SDI_WiM-( (1/d)*gbw )
            #
            if (SDI_WiM < SDI_NoM )
            {
                print("final comparison")
                j<-org
                o[j] <- a[i]
                j <- j+1
                o[j]<-NA
                l<-i+1
            }
            print("###")
            res <- rbind(res,c(i,j,l,SDI_NoM,gbw,SDI_WiM))
            print(res)
            print(o)
        }
        i <- i+1
        #
        if (is.na(a[i]))
        {
            print("enter a is finished")
            while (l <= length(b))
            {
                if( ( length(intersect(b[1:l],o[1:j])) / length(union(b[1:l],o[1:j])) ) > as.numeric(treshold))
                {
                    print("reached min similarity")
                    o[j] <- NA
                    o[j+1] <- NA
                    break;
                    
                }
                print("a is finished")
                o[j] <- b[l]
                print(o)
                l <- l+1
                j <- j+1
            }
        }
        o[j] <- NA
        o[j+1] <- NA
    }
    return(o)
}