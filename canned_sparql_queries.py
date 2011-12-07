# file canned_sparql_query.py
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
'''
This file contains a dictionary of predefined SPARQL queries, 
available for the run_sparql_query command.
'''

sample_sparql_query={}
sample_sparql_query['get_types']='SELECT DISTINCT ?type WHERE { ?thing a ?type . } ORDER BY ?type'  
sample_sparql_query['find_subtypes']="""
PREFIX scx:<http://galyn.example.com/source_data_files/setup_Complex.csv#>
PREFIX sxcxcx:<http://galyn.example.com/source_data_files/setup_xref_Complex-Complex.csv#>
PREFIX sxsxcx:<http://galyn.example.com/source_data_files/setup_xref_Simplex-Complex.csv#>
PREFIX ssx:<http://galyn.example.com/source_data_files/setup_Simplex.csv#> 
select * where {
  {
    ?sxcxcx sxcxcx:HigherComplex scx:r1;
            sxcxcx:Name ?name;
            sxcxcx:LowerComplex ?lower.
    ?lower scx:GrammarRule_Text ?rule.
  } UNION {
    ?sxsxcx sxsxcx:Complex scx:r1;
            sxsxcx:Simplex ?ssx.
    ?ssx ssx:Name ?name.
  }
}
"""

# This query works in the GUI, but not in the API
sample_sparql_query['find_events_order_time']="""
PREFIX dcx:<http://galyn.example.com/source_data_files/data_Complex.csv#>
PREFIX scx:<http://galyn.example.com/source_data_files/setup_Complex.csv#>
PREFIX ssx:<http://galyn.example.com/source_data_files/setup_Simplex.csv#>
PREFIX sxcxcx:<http://galyn.example.com/source_data_files/setup_xref_Complex-Complex.csv#>
SELECT ?macro ?melabel ?event ?evlabel (MIN(?evdate) as ?mindate)
WHERE {
  ?macro a scx:r1;                  
         dcx:Identifier ?melabel;
         sxcxcx:r61 ?event.         
  ?event dcx:Identifier ?evlabel;
         sxcxcx:r62 ?_1.            
  ?_1 sxcxcx:r64 ?_2.               
  {
    ?_2 sxcxcx:r78 ?_3. 
    ?_3 sxcxcx:r103 ?_4. 
    ?_4 sxcxcx:r104 ?_5. 
  } UNION {
    ?_2 sxcxcx:r47 ?_6.    
    ?_6 sxcxcx:r79 ?_7. 
    ?_7 sxcxcx:r103 ?_8. 
    ?_8 sxcxcx:r104 ?_5. 
  } UNION {
    ?_2 sxcxcx:r47 ?_6.    
    ?_6 sxcxcx:r80 ?_9. 
    ?_9 sxcxcx:52 ?_7.    
    ?_7 sxcxcx:r103 ?_8. 
    ?_8 sxcxcx:r104 ?_5. 
  } UNION {
    ?_2 sxcxcx:r47 ?_6.    
    ?_6 sxcxcx:r80 ?_9. 
    ?_9 sxcxcx:r53 ?_10. 
    ?_10 sxcxcx:r60 ?_5. 
  }

  ?_5 sxcxcx:r20 ?_11.  

  {
    ?_11 sxcxcx:r97 ?_12.     
    ?_12 ssx:r66 ?evdate      
  } UNION {
    ?_11 sxcxcx:r22 ?_13.     
    ?_13 sxcxcx:r4 ?_14.      
    ?_14 ssx:r66 ?evdate      
  } UNION {
    ?_11 sxcxcx:r22 ?_13.     
    ?_13 sxcxcx:r4 ?_14.      
    ?_14 ssx:r68 ?evdate 
  }
}
GROUP BY ?macro ?melabel ?event ?evlabel
ORDER BY ?mindate
"""
sample_sparql_query['find_event_order_location']="""
PREFIX dcx:<http://galyn.example.com/source_data_files/data_Complex.csv#>
PREFIX scx:<http://galyn.example.com/source_data_files/setup_Complex.csv#>
PREFIX ssx:<http://galyn.example.com/source_data_files/setup_Simplex.csv#>
PREFIX sxcxcx:<http://galyn.example.com/source_data_files/setup_xref_Complex-Complex.csv#>
SELECT DISTINCT ?state ?county ?city ?event ?evlabel ?macro ?melabel
WHERE {
  ?macro a scx:r1;      
         dcx:Identifier ?melabel;
         sxcxcx:r61 ?event. 
  ?event dcx:Identifier ?evlabel;
         sxcxcx:r62 ?_1.   
  ?_1 sxcxcx:r64 ?_2.    

  {
    ?_2 sxcxcx:r78 ?_3.  
    ?_3 sxcxcx:r103 ?_4.  
    ?_4 sxcxcx:r106 ?_5. 
  } UNION {
    ?_2 sxcxcx:r47 ?_6. 
    ?_6 sxcxcx:r79 ?_3. 
    ?_3 sxcxcx:r103 ?_4. 
    ?_4 sxcxcx:r106 ?_5. 
  } UNION {
    ?_2 sxcxcx:r47 ?_6.      
    ?_6 sxcxcx:r80 ?_7.     
    ?_7 sxcxcx:52 ?_3.      
    ?_3 sxcxcx:r103 ?_4.    
    ?_4 sxcxcx:r106 ?_5.     
  } UNION {
    ?_2 sxcxcx:r47 ?_6.      
    ?_6 sxcxcx:r80 ?_7.     
    ?_7 sxcxcx:r53 ?_8.      
    ?_8 sxcxcx:r59 ?_5.      
  }
  {
    ?_5 sxcxcx:r2 ?_9.               
    ?_9 sxcxcx:r41 ?_10.              
  } UNION {
    ?_5 sxcxcx:r3 ?_10.               
  }
  
  OPTIONAL {
    ?_10 ssx:r18 ?county.             
    FILTER (?county != "?")
  }
  OPTIONAL {
    ?_10 ssx:r30 ?state.              
    FILTER (?state != "?")
  }
  OPTIONAL {
    ?_10 ssx:r55 ?city.              
    FILTER (?city != "?")
  }
  
  FILTER (BOUND(?state) || BOUND(?county) || BOUND(?city))
}
ORDER BY UCASE(?state) UCASE(?county) UCASE(?city) ?event ?evlabel 
"""
sample_sparql_query['find_articles_for_event']="""
PREFIX dcx:<http://galyn.example.com/source_data_files/data_Complex.csv#>
PREFIX dxcxd:<http://galyn.example.com/source_data_files/data_xref_Complex-Document.csv#>
PREFIX scx:<http://galyn.example.com/source_data_files/setup_Complex.csv#>
PREFIX ssx:<http://galyn.example.com/source_data_files/setup_Simplex.csv#>
PREFIX sxcxcx:<http://galyn.example.com/source_data_files/setup_xref_Complex-Complex.csv#>
SELECT ?macro ?melabel ?event ?evlabel ?dd ?docpath 
WHERE {
  ?macro a scx:r1;                  
         dcx:Identifier ?melabel;
         sxcxcx:r61 ?event.         
  ?event dcx:Identifier ?evlabel.
  ?dxcxd dxcxd:Complex ?event;
         dxcxd:Document ?dd.
  ?dd ssx:r85 ?docpath.   
} 
ORDER BY ?macro ?event ?docpath
"""
sample_sparql_query['find_events_for_specific_person']="""
PREFIX dcx:<http://galyn.example.com/source_data_files/data_Complex.csv#>
PREFIX sxcxcx:<http://galyn.example.com/source_data_files/setup_xref_Complex-Complex.csv#>
SELECT ?triplet ?role ?trlabel ?event ?evlabel ?macro ?melabel 
WHERE {
  dcx:r4569 ^sxcxcx:r31 ?actor. 
  {
    ?actor ^sxcxcx:r30 ?participant. 
    ?triplet sxcxcx:r63 ?participant. 
    BIND("subject" as ?role)
  } UNION {
    ?actor ^sxcxcx:r35 ?participant.  
    ?triplet sxcxcx:r65 ?participant.  
    BIND("object" as ?role)
  } 

  ?triplet dcx:Identifier ?trlabel.
  ?event sxcxcx:r62 ?triplet;       
         dcx:Identifier ?evlabel.
  ?macro sxcxcx:r61 ?event;          
         dcx:Identifier ?melabel.      
}
"""

'''
PREFIX dcx:<http://galyn.example.com/source_data_files/data_Complex.csv#>
PREFIX dd:<http://galyn.example.com/source_data_files/data_Document.csv#>
PREFIX dsxd:<http://galyn.example.com/source_data_files/data_SimplexDate.csv#>
PREFIX dsxn:<http://galyn.example.com/source_data_files/data_SimplexNumber.csv#>
PREFIX dsxt:<http://galyn.example.com/source_data_files/data_SimplexText.csv#>
PREFIX dsx:<http://galyn.example.com/source_data_files/data_Simplex.csv#>
PREFIX dttcu:<http://galyn.example.com/source_data_files/data_TempTranslatorCU.csv#>
PREFIX dvcta:<http://galyn.example.com/source_data_files/data_VCommentArchive.csv#>
PREFIX dxacxcx:<http://galyn.example.com/source_data_files/data_xref_AnyComplex-Complex.csv#>
PREFIX dxctcx:<http://galyn.example.com/source_data_files/data_xref_comment-complex.csv#>
PREFIX dxctd:<http://galyn.example.com/source_data_files/data_xref_Comment-Document.csv#>
PREFIX dxctsx:<http://galyn.example.com/source_data_files/data_xref_Comment-Simplex.csv#>
PREFIX dxcxcx:<http://galyn.example.com/source_data_files/data_xref_Complex-Complex.csv#>
PREFIX dxcxd:<http://galyn.example.com/source_data_files/data_xref_Complex-Document.csv#>
PREFIX dxsxcx:<http://galyn.example.com/source_data_files/data_xref_Simplex-Complex.csv#>
PREFIX dxsxd:<http://galyn.example.com/source_data_files/data_xref_Simplex-Document.csv#>
PREFIX dxsxsxd:<http://galyn.example.com/source_data_files/data_xref_Simplex-Simplex-Document.csv#>
PREFIX dxvctd:<http://galyn.example.com/source_data_files/data_xref_VComment-Document.csv#>
PREFIX dxvct:<http://galyn.example.com/source_data_files/data_xref_VComment.csv#>
PREFIX scx:<http://galyn.example.com/source_data_files/setup_Complex.csv#>
PREFIX sd:<http://galyn.example.com/source_data_files/setup_Document.csv#>
PREFIX ssx:<http://galyn.example.com/source_data_files/setup_Simplex.csv#>
PREFIX sxcxcx:<http://galyn.example.com/source_data_files/setup_xref_Complex-Complex.csv#>
PREFIX sxsxcx:<http://galyn.example.com/source_data_files/setup_xref_Simplex-Complex.csv#>
PREFIX sxsxd:<http://galyn.example.com/source_data_files/setup_xref_Simplex-Document.csv#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
'''

# EMP DEPT REPOSITORY SPARQL QUERIES
 
# 01 List all employees
sample_sparql_query['emp_dept_01']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?emp where {
?emp  rdf:type  f:emp.
}
"""

# 02 List the names of all employees in alphabetical order
sample_sparql_query['emp_dept_02']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?name where {
?emp  rdf:type  f:emp.
?emp  foaf:surname ?name. 
}
ORDER BY ?name
"""

# 03 List the employees' name, salary, department number and job
# Note that ; in place of . repeats the subject.
sample_sparql_query['emp_dept_03']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?name ?sal ?dno ?job where {
?emp  rdf:type  f:emp;
    foaf:surname ?name;
    f:Sal ?sal;
    f:Dept ?dept;
    f:Job ?job.  
?dept f:DeptNo ?dno. 
}
"""

# FAILS
# 04 List the first 5 employees
sample_sparql_query['emp_dept_04']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?ename where {
?emp  rdf:type  f:emp;
    foaf:surname ?ename.
} 
ORDER BY ?ename
LIMIT 5
"""

# 04a List the first 5 employees
sample_sparql_query['emp_dept_04a']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?ename where {
?emp  rdf:type  f:emp;
    foaf:surname ?ename.
} 
ORDER BY ?ename
"""

# 04b List the first 5 employees
sample_sparql_query['emp_dept_04b']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?ename where {
?emp  rdf:type  f:emp;
    foaf:surname ?ename.
} 
LIMIT 5
"""

# 05 List the top 5 employees by salary
sample_sparql_query['emp_dept_05']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?ename ?sal where {
?emp  rdf:type  f:emp;
   foaf:surname ?ename;
   f:Sal ?sal.
} 
ORDER BY DESC(?sal)
LIMIT 5
"""

# 06 List the departments
sample_sparql_query['emp_dept_06']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?dept where {
?dept  rdf:type  f:dept.  
}
"""

# 07 List all departments and all employees
sample_sparql_query['emp_dept_07']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?dept ?emp where {
{?dept  rdf:type  f:dept }
UNION
{?emp rdf:type f:emp}
}
"""

# 08 List the employees with salaries over 1000
# If the RDF literal is typed, for example as xs:integer as is the case with this generated RDF, 
# then the following query will select employees with a salary greater than 1000
sample_sparql_query['emp_dept_08']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?emp ?sal where {
?emp  rdf:type  f:emp;
    f:Sal ?sal.
FILTER (?sal > 1000)
}
"""

# 09 List the employees with salaries over 1000
# If the RDF literal is not typed, then the variable must be cast
sample_sparql_query['emp_dept_09']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
prefix xs: <http://www.w3.org/2001/XMLSchema#>
select ?emp ?sal where {
?emp  rdf:type  f:emp;
    f:Sal ?sal.
FILTER (xs:integer(?sal) > 1000)
}
"""

# 10 List employees and their locations
sample_sparql_query['emp_dept_10']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?emp ?loc where {
?emp  rdf:type  f:emp.
?emp f:Dept ?dept.
?dept f:Location ?loc.
}
"""

# 11 List the names of employees and their managers
sample_sparql_query['emp_dept_11']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?ename ?mname where {
?emp  rdf:type  f:emp;
    f:Mgr ?mgr;
    foaf:surname ?ename.
?mgr foaf:surname ?mname.
} 
"""

# 12 List the names of employees and their managers
# Include employees with no manager
sample_sparql_query['emp_dept_12']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?ename ?mname where {
?emp  rdf:type  f:emp;
    foaf:surname ?ename.
OPTIONAL {?emp f:Mgr ?mgr.
        ?mgr foaf:surname ?mname.
       }
}
"""

# 13 List employees with no manager
# Result: ename = "KING"
sample_sparql_query['emp_dept_13']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?ename where {
?emp  rdf:type  f:emp;
    foaf:surname ?ename.
OPTIONAL {?emp f:Mgr ?mgr}
FILTER (!bound(?mgr))
}
"""

# 14 List the distinct locations of staff
# Result: loc
# <file://dbpedia.org/resource/New_York>
# <file://dbpedia.org/resource/Dallas>
# <file://dbpedia.org/resource/Chicago>
sample_sparql_query['emp_dept_14']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select distinct ?loc  where {
?emp  rdf:type  f:emp.
?emp  f:Dept ?dept.
?dept f:Location ?loc.
}
"""

# 15 List details of the employees who are ANALYSTs
sample_sparql_query['emp_dept_15']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select * where {
?emp  rdf:type  f:emp.
?emp  f:Dept ?dept.
?dept f:Location ?loc.
?emp f:Job ?job.
FILTER (?job = "ANALYST")
}
"""

# 16 List employees who are either ANALYSTs or MANAGERs
sample_sparql_query['emp_dept_16']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?emp where {
?emp  rdf:type  f:emp;
    f:Job ?job.
FILTER (?job = "ANALYST"  || ?job = "MANAGER")
}
"""

# 17 List employees who are neither ANALYSTs nor MANAGERs
sample_sparql_query['emp_dept_17']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select * where {
?emp  rdf:type  f:emp;
     f:Job ?job.
FILTER (?job != "ANALYST"  && ?job != "MANAGER")
}
"""

# 18  List employees whose surname begins with "S"
# Result: emp                                   ename
# <http://www.cems.uwe.ac.uk/empdept/emp/7369>  "SMITH"
# <http://www.cems.uwe.ac.uk/empdept/emp/7788>  "SCOTT"
sample_sparql_query['emp_dept_18']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select * where {
?emp  rdf:type  f:emp.
?emp foaf:surname ?ename.
FILTER (regex(?ename, "^S"))
} 
"""

# 19 List employees whose surname contains "AR"
# Result: emp                                   ename
# <http://www.cems.uwe.ac.uk/empdept/emp/7521>  "WARD"
# <http://www.cems.uwe.ac.uk/empdept/emp/7782>  "CLARK"
# <http://www.cems.uwe.ac.uk/empdept/emp/7654>  "MARTIN"
sample_sparql_query['emp_dept_19']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select * where {
?emp  rdf:type  f:emp.
?emp foaf:surname ?ename.
FILTER (regex(?ename, "AR"))
}
"""

# 20 List employees whose surname contains M followed by R ignoring case
# Result:   emp                                 ename
# <http://www.cems.uwe.ac.uk/empdept/emp/7934> "MILLER"
# <http://www.cems.uwe.ac.uk/empdept/emp/7654> "MARTIN"
sample_sparql_query['emp_dept_20']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select * where {
?emp  rdf:type  f:emp.
?emp foaf:surname ?ename.
FILTER (regex(?ename, "m.*r","i"))
}
"""

# 21  Compute the maximum salary (SPARQL 1.1)
# Result: MaxSal=5000
sample_sparql_query['emp_dept_21']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select (max(?sal) as ?maxsal) where {
?maxemp  rdf:type  f:emp.
?maxemp  f:Sal ?sal.
}
"""

# 22 Compute employees with the same salary
sample_sparql_query['emp_dept_22']="""
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select * where {
?emp1 f:Sal ?sal.
?emp2 f:Sal ?sal.
FILTER (?emp1 != ?emp2)
}
"""

# 23 Get the department which SMITH works for
sample_sparql_query['emp_dept_23']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?dname  where {
?emp  rdf:type  f:emp.
?emp f:Dept ?dept.
?emp foaf:surname "SMITH".
?dept f:Dname ?dname.
}
"""

# 24 List the names of employees in Accounting
sample_sparql_query['emp_dept_24']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?ename  where {
?emp  rdf:type  f:emp.
?emp f:Dept ?dept.
?emp foaf:surname ?ename.
?dept f:Dname "Accounting".
} 
"""

# 25 Employees hired in this millennium
# Note that the literal needs to be typed to make this comparison work.
sample_sparql_query['emp_dept_25']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
prefix xs: <http://www.w3.org/2001/XMLSchema#>
select ?ename ?hire where {
?emp  rdf:type  f:emp.
?emp f:HireDate ?hire.
?emp foaf:surname ?ename.
FILTER (?hire > "2000-01-01"^^xs:date) 
}
"""

# 26 List the names of employees whose manager is in a different department
sample_sparql_query['emp_dept_26']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?name ?edname ?mdname {
  ?emp  rdf:type  f:emp;
        foaf:surname ?name;
        f:Dept ?dept;
        f:Mgr ?mgr.
  
   ?mgr f:Dept ?mdept. 
   ?dept f:Dname ?edname.
   ?mdept f:Dname ?mdname.
   FILTER (?dept != ?mdept)
}
"""

# 27 List the grades of employees
# In relational terms, this is a theta-join between the employee and the salgrade tables
sample_sparql_query['emp_dept_27']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?ename ?grade where {
?emp  rdf:type  f:emp;
   foaf:surname ?ename;
   f:Sal ?sal.
?salgrade rdf:type f:salgrade; 
   f:LoSal ?low; 
   f:HiSal ?high;
   f:Grade ?grade.

FILTER (?sal >= ?low && ?sal <= ?high)
}
"""

# 28 Abbreviated query syntax
# No prefix would be:
#select ?sal  where { <http://www.cems.uwe.ac.uk/empdept/emp/7900> f:Sal ?sal. }
sample_sparql_query['emp_dept_28']="""
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
prefix e: <http://www.cems.uwe.ac.uk/empdept/emp/>
select ?sal  where {
e:7900 f:Sal ?sal.
}
"""

# 29 introduce a default namespace
sample_sparql_query['emp_dept_29']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix : <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?name ?sal ?dno ?job where {
?emp  rdf:type  :emp;
   foaf:surname ?name;
   :Sal ?sal;
   :Dept ?dept;
   :Job ?job.  
?dept :DeptNo ?dno. 
}
"""

# 30 use the abbreviation a for rdf:type
sample_sparql_query['emp_dept_30']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix : <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?name ?sal ?dno ?job where {
?emp  a :emp;
   foaf:surname ?name;
   :Sal ?sal;
   :Dept ?dept;
   :Job ?job.  
?dept :DeptNo ?dno. 
}
"""

# 31 if we don't need to return the resource itself, it can be anonymous
sample_sparql_query['emp_dept_31']="""
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix : <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?name ?sal ?dno ?job where {
[ a :emp;
foaf:surname ?name;
:Sal ?sal;
:Dept ?dept;
:Job ?job
].
?dept :DeptNo ?dno. 
}
"""

## Aggregation functions like count() and sum() and the GROUP BY clause are not defined in SPARQL 1.0

# 32 Count the number of departments
sample_sparql_query['emp_dept_32']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select (count(?dept) as ?count) where {
?dept  rdf:type  f:dept.
}
"""
# 33 Count the number of employees in each department
sample_sparql_query['emp_dept_33']="""
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select distinct ?dept (count(?emp) as ?count) where {
?dept a f:dept.
?emp f:Dept ?dept.
} group by ?dept
"""

## Generic queries

# 34 List all data
sample_sparql_query['emp_dept_34']="""
select * where {
?s ?p ?o
}
"""

# 35 List all data LIMIT 20
sample_sparql_query['emp_dept_35']="""
select * where {
?s ?p ?o
} LIMIT 20

"""

# 36 List all employee data
sample_sparql_query['emp_dept_36']="""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?prop ?val where {
?emp  rdf:type  f:emp.
?emp ?prop ?val.
}
"""

# 37 What types are there?
# Note: This shows that triples defining the emp vocabulary are in the same dataset.
sample_sparql_query['emp_dept_37']="""
select distinct ?type where {
?s a ?type
}
"""

# 38 What properties are there?
# This query only finds ranges which are instances of a type in the dataset. 
# Sal has a range of xs:integer but it is not easy to discover that with a SPARQL query.
sample_sparql_query['emp_dept_38']="""
select distinct ?prop where {
?s ?prop ?o
}
"""

# 39 What is the domain(s) of a property?
sample_sparql_query['emp_dept_39']="""
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select distinct ?type where {
?s f:Sal ?v.
?s a ?type.
}
"""

# 40 What are the ranges of a property (Sal)?
sample_sparql_query['emp_dept_40']="""
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select distinct ?type where {
?s f:Sal ?o.
?o a ?type.
}
"""

# 41  What are the ranges of a property (Mgr)?
sample_sparql_query['emp_dept_41']="""
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select distinct ?type where {
?s f:Mgr ?o.
?o a ?type.
}
"""

# 42 What properties have a given type as its domain ?
sample_sparql_query['emp_dept_42']="""
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select distinct ?prop where {
 ?s a f:salgrade.
 ?s ?prop [].
}
"""

## Schema queries
## The presence of schema data enables SPARQL to be used to query this meta-data.

# 43 What properties have a domain of a given type?
# Note that this has only returned the properties in the empdept vocab, 
# not the foaf name property used in the raw data.
sample_sparql_query['emp_dept_43']="""
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?prop  where {
?prop rdfs:domain f:emp.
}
"""

# 44 What integer properties do employees have?
sample_sparql_query['emp_dept_44']="""
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
prefix xs: <http://www.w3.org/2001/XMLSchema#>
select ?prop  where {
?prop rdfs:domain f:emp.
?prop rdfs:range xs:integer.
}
"""

# 45 What types of resources have salaries?
sample_sparql_query['emp_dept_45']="""
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select ?type where {
f:Sal rdfs:domain ?type.
}
"""

## Queries on both the data and the vocab can be made

# 46 What literal properties do MANAGERS have?
sample_sparql_query['emp_dept_46']="""
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix f: <http://www.cems.uwe.ac.uk/empdept/concept/>
select DISTINCT ?prop  where {
?x f:Job "MANAGER".
?x a ?type. 
?prop rdfs:domain ?type.
?prop rdfs:range rdfs:literal.
}
"""


