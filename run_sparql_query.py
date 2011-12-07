'''
**run_sparql_query** is a manage.py script to send SPARQL queries 
to the triplestore using the API

Examples usage
^^^^^^^^^^^^^^

Run help to see a list of keys available for the canned_sparql_queries::

  $ python run_sparql_query.py -h
  
Get a list of available repositories from the triplestore::

  $ python run_sparql_query.py -l

Run a SPARQL query from the canned_sparql_queries::

  $ python run_sparql_query.py -q emp_dept_01
  
  $ python run_sparql_query.py -r galyn-2011-11-07 -q find_event_order_location
  $ python run_sparql_query.py -r galyn-2011-11-07 -q find_events_for_specific_person
  $ python run_sparql_query.py -r galyn-2011-11-07 -q find_articles_for_event
  
Run a SPARQL query loaded from a file::

  $ python run_sparql_query.py -f load_sparql_query.txt

----
'''

import argparse
from pprint import pprint
import logging
import sys

import sesameConnection
import canned_sparql_queries
        
if __name__ == '__main__':
    
    query_key_help='Load sparql query predefined query keys:\n%s\n' % canned_sparql_queries.sample_sparql_query.keys()    

    import argparse
    '''Load command line arguments'''
    # Query make be defined as key to predefined queries, or file containing query.
    parser = argparse.ArgumentParser(epilog="Example: python run_sparql_query.py -l -o -p -v DEBUG")
    parser.add_argument('-f', '--query_file', nargs=1, help='Load sparql query from file', dest='query_file')  
    parser.add_argument('-l', '--list_repos', help='Get a list of available repositories', action='store_true') 
    #parser.add_argument('-o', '--output', help='Output will be saved to a file', default=None, action='store_true')
    #parser.add_argument('-p', '--ppdict', help='Pretty print the resulting dictionary', default=False, action='store_true')
    parser.add_argument('-q', '--query_key', nargs=1, help=query_key_help, dest='query_key', choices=canned_sparql_queries.sample_sparql_query.keys())
    parser.add_argument('-r', '--repository', nargs=1, help='Sesame Repository', default=['emp_dept'])  
    parser.add_argument('-u', '--url', nargs=1, help='Sesame URL', dest='sesame_url', default=['http://localhost:8180/openrdf-sesame/'], required=False)    
    parser.add_argument('-v', '--loglevel', required=False, choices=['ERR', 'WARN', 'INFO', 'DEBUG'], default='DEBUG', help='Log level for additional output.')
    parser.add_argument('-g', '--logpath', nargs=1, required=False, default=None, help='Log path, defaulta to stdout, if not specificed.')
     
    # parse_args returns a namespace, which is an object created to hold attributes.
    args = parser.parse_args()
    print args
    
    # Open a Sesame connection
    sc = sesameConnection.OpenSesame(args)
    
    # Send a sparql query to sesame
    sparql_query = sc.construct_query(args)
    if args.query_key is None: outputfile = "result_sparql_query"
    else: outputfile = ''.join(['results_', args.query_key[0]])
    
    # Run the SPARQL query
    sparql_query = sc.construct_query(args)
    if sparql_query is None:
        result = sc.sesame_query(result_type="SPARQL_XML", request_method='GET', output=outputfile) 
    else: 
        result = sc.sesame_query(result_type="SPARQL_XML", request_method='POST', output=outputfile, sparql_query=sparql_query)
