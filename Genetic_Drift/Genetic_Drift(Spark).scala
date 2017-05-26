val gamete_rate = 100
val offspr_rate = 100
val generations = 300
 
var frequency: List[Double] = List()
var individuals = sc.parallelize(List.fill(50)("0") ++ List.fill(50)("1"))
 
for(generation <- 1 to generations){
  val gametes = individuals.flatMap(x => (x * gamete_rate).split("").tail)
  individuals = sc.parallelize(gametes.takeSample(false, offspr_rate))
  val count = individuals.countByValue
  frequency = frequency :+ count("1").toDouble / offspr_rate
}
 
print(frequency)
