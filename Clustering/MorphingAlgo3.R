ShapeMorphingPositive <- function(s,t,d)
{
    j <-1 
    k <- 1
    o <- vector()
    ##
    for( i in 1:length(s))
    {
        if( is.na(s[i]))
        {
            print("NA")
            o[k] <- NA
            k<-k+1
        }
        else if( s[i] == t[j] )
        {
            print("equal case")
            o[k] <- t[j]
            k<-k+1
            j<-j+1
        }
        else if( abs(s[i]) < abs(t[j]) )
        {
            print("a is greater")
            bwo <- ( abs(t[j]-s[i]) / ( max(s[1:i],t[1:j]) - min(s[1:i],t[1:j]) ) )
            ##
            o[k] <- s[i]
            JC_woM <-  ( length(intersect(t[1:j],o[1:k])) / length(union(t[1:j],o[1:k]))  )
            o[k] <- NA
            ##
            o[k] <- t[j]
            JC_wiM <-  ( length(intersect(t[1:j],o[1:k])) / length(union(t[1:j],o[1:k]))  ) - ((1/d)*bwo)
            o[k] <- NA
            cat("JC_wiM= ",JC_wiM,"\n")
            cat("JC_woM= ",JC_woM,"\n")
            cat("bwo= ",bwo,"\n")
            if(JC_woM > JC_wiM)
            {
                o[k] <- s[i]    
            }
            else
            {
                o[k] <- t[j]   
            }
            j <- j+1
            k <- k+1
            
        }
        else if( a[i] > b[j])
        {
            
        }
        else
        {
            print("error")
        }
    }
    return(o)
}