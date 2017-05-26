import scala.util.Random
import scala.collection.mutable.ListBuffer
 
val gamete_rate = 100
val offspr_rate = 100
val generations = 1000
 
var frequency: List[Double] = List()
 
var individuals = List.fill(50)(0) ++ List.fill(50)(1)
 
for(generation <- 1 to generations){
  var gametes = individuals.map(x => List.fill(gamete_rate)(x)).flatten
  individuals = Random.shuffle(gametes).take(offspr_rate)
  frequency = frequency :+ individuals.count(_ == 1).toDouble / offspr_rate
}
 
print(frequency)
