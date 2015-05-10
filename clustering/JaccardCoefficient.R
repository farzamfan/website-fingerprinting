JacCoeff <- function(t1,t2,t3)
{
    cat("t1,t3",length(intersect(t1,t3))/length(union(t1,t3)),"\n")
    cat("t2,t3",length(intersect(t2,t3))/length(union(t2,t3)),"\n")
}