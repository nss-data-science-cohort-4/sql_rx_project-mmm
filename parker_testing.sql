-- 4 (MATT) Is there an association between rates of 
--opioid prescriptions and overdose deaths by county?

--Total claims per generic_name
--NEEDS WORK - Add group by for including a drug name
SELECT SUM(p.total_claim_count)
	, d.generic_name
FROM prescription AS p 
INNER JOIN drug AS d
USING(drug_name)
WHERE d.opioid_drug_flag = 'Y'
GROUP BY generic_name
ORDER BY generic_name, sum;

--Look into deaths by county
SELECT f.county
	, year
	, p.population
	, overdose_deaths
	, ROUND(overdose_deaths / population * 1000.0, 3) AS deaths_per_thousand
FROM overdose_deaths AS o
JOIN fips_county AS f
USING(fipscounty)
JOIN population AS p
USING(fipscounty)
ORDER BY deaths_per_thousand DESC;
--ORDER BY f.county, year DESC;




