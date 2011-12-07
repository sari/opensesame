# file sesameConnection.py
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
Objects to interact with the Sesame Triplestore in order to
run SPARQL queries against the Sesame repository content.

'''

import argparse
from datetime import datetime
import httplib2
import json
import logging
import os
from pprint import pprint
import re
import sys
from urllib import urlencode
import xml.dom.minidom
from xml.dom.minidom import Node

import canned_sparql_queries

logger = logging.getLogger(__name__)

class OpenSesameException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class OpenSesame():
    
    def __init__(self, args):
        # configure logging
        self.hdlr  = None
        self.repository = args.repository[0]            
        self.url = args.sesame_url[0]        
        self.setLogger(args)     
        self.logger.info('SesameConnection starting up...')        
    
    def close(self):
        self.logger.info('...SesameConnection closing down.')
        self.logger.removeHandler(self.hdlr)       

    def setLogger(self, args):     
        levelDict = {'DEBUG':logging.DEBUG,
                     'INFO':logging.INFO,
                     'WARN':logging.WARNING,
                     'ERR':logging.ERROR}
        self.logger = logging.getLogger()

        # set the output to either stderr or log file
        if args.logpath is None: # default set log output to stderr
            self.hdlr = logging.StreamHandler(sys.stderr)
        else: # self.hdlr is path to log file.
            self.hdlr = logging.FileHandler(self.logPath)
        # set the log output format
        #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')            
        formatter = logging.Formatter('%(levelname)s: %(message)s')            
        self.hdlr.setFormatter(formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(levelDict[args.loglevel]) 
        # don't propagate to root logger
        self.logger.propagate = False

    def construct_query(self, args):

        if args.query_key: 
            'Use one of the predefined sparql queries bases on given key.'
            logger.debug("QUERY KEY=[%s]" % args.query_key[0])
            sparql_query=canned_sparql_queries.sample_sparql_query[args.query_key[0]]           

        elif args.query_file: 
            'Load the sparql query from the given file.'
            logger.debug("QUERY FILE=[%s]" % args.query_file[0])
            try:
                sparql_query=open(args.query_file[0], 'rU').read()
            except IOError as (errno, strerror):
                raise OpenSesameException("Failed to read query file [%s]" % args.query_file[0]) 
                
        elif args.list_repos: 
            'Query for a list of available repositories.'
            logger.debug('Query for a list of available repositories.')
            sparql_query=None                 
                        
        else: 
            'No query given, so get a list of the repositories in the triplestore.'
            logger.debug("No options, get list of repositories.")
            sparql_query=None            
            
        return sparql_query
        
    def post_query(self, args, query):      
        result={}
        try:
            filename = args.query_key[0] if args.query_key else None
            print "filename = [%s]" % filename
            if self.query: # Run the defined sparql query           
                result = self.post_query(result_type="SPARQL_XML", request_method="POST", sparql_query=squery, output=filename)
            elif self.list_repos: # Query the triplestore for available repositories
                result = self.post_query(result_type="SPARQL_XML", request_method="GET", sparql_query=None, output=filename)
            else: logger.error('Query not found.')  # Error: Query not found.
        except: OpenSesameException("Failed to run SparqlStore query.")  
        return result
        
    def getResultType(self, type):
        if type=='SPARQL_XML':  return 'application/sparql-results+xml'
        elif type=='SPARQL_JSON':  return 'application/sparql-results+json' 
        elif type=='BINARY_TABLE':  return 'application/x-binary-rdf-results-table' 
        elif type=='BOOLEAN':  return 'text/boolean'

    def sesame_query(self, result_type="SPARQL_XML", request_method="POST", output=None, sparql_query=None):
        'Send a SPARQL query to the triplestore'
        
        logger.debug("query begin ... result_type=[%s]" % result_type)

        # set the content-type and accept headers 
        headers = { 
          'content-type': 'application/x-www-form-urlencoded',      
          'accept': self.getResultType(result_type)
        }
        # create the endpoint      
        endpoint = "%s/repositories" % (self.url)
        logger.debug("query endpoint=[%s]" % endpoint)        
        
        if sparql_query:
            # remove any newlines from sparql_query string
            sparql_query = sparql_query.translate(None,'\n')
            # add query to params              
            params = { 'query': sparql_query }            
            endpoint += "/%s" % (self.repository)
        else: 
            '''If no query is defined, an api call will be made
               to list the triplestore repositories available.'''
            params = {}                            
            request_method = 'GET'
            
        logger.debug('query %s to %s' % (request_method, endpoint))
        
        try:
            # send the query to the api
            (response, content) = self.doRequest(endpoint, request_method, params, headers) 
            logger.debug("Response Status = %s" % (response.status))
            
            # Output the xml to a file 
            if output:
                try:
                    outputfile = ''.join(['results/', output, ".xml"])
                    logger.debug("writing response to file = [%s]\n" % outputfile)
                    a = open(outputfile, 'w')
                    a.write(content) 
                except IOError as (errno, strerror):
                    logger.error("I/O error({0}): {1}".format(errno, strerror))
                    logger.error("Failed to open query output file [%s]\n" % outputfile)
                    return
            
            # output the full response for now
            #pprint(response)
            logger.debug("Content Length = %s" % (len(content)))                   
                    
            if (response.status == 200):
                'HTML Response OK'
                if (result_type == 'SPARQL_XML'):
                    'XML Results Output'    
                    logger.debug("Result type is SPARQL_XML, before call to Xml2Dict")             
                    return self.Xml2Dict(content, output)                  
                elif (result_type == 'SPARQL_JSON'):
                    'JSON Results Output'
                    logger.debug("Result type is SPARQL_JSON")                  
                    return json.loads(content)
            else:
                'HTML Response not OK'      
                logger.error('HTTP Response error code: %s' % response.status)            
                match = re.search(r'<b>message</b> <u>([^<]+)<', content)            
                if match:
                    logger.error('HTTP Response error message = [%s]' % match.group(1))      
                match = re.search(r'<b>description</b> <u>([^<]+)<', content)            
                if match: 
                    error_desc='raise Exception description = [%s]' % match.group(1)
                    logger.error(error_desc)
                    raise OpenSesameException(error_desc)
                else:
                    logger.error('HTTP Response failed with response code = [%s]' % response)
                    logger.error('raise Exception [%s ...]' % content[:50])  # only show first 30 chars
                    raise OpenSesameException(content)
        except httplib2.ServerNotFoundError:
            raise OpenSesameException("Site is Down: %s" % self.url)                                             
        
        
    def doRequest(self, endpoint, request_method, params, headers):
        (response, content) = httplib2.Http().request(endpoint, request_method, urlencode(params), headers=headers)
        logger.debug('HTTP request endpoint=[%s]' % endpoint)
        logger.debug('HTTP request request_method=[%s]' % request_method)  
        logger.debug('HTTP request headers=[%s]' % headers) 
        logger.debug('HTTP response=[%s]' % response)
        return (response, content)        
        
    def Xml2Dict(self, content, output=None):
        '''Parse the SPARQL query result content into a dictionary.'''
        doc = xml.dom.minidom.parseString(content)
        mapping=[]

        for node in doc.getElementsByTagName("result"):
            binding={}
            L2 = node.getElementsByTagName("binding")
            for node2 in L2:
                item={}
                key1 = node2.getAttribute("name")
                if (node2.getElementsByTagName("uri")): 
                    item['type']="uri"
                    
                elif (node2.getElementsByTagName("literal")):
                    item['type']="literal"
                    type2 = "literal"
                    if node2.getAttribute("datatype"):
                        logger.debug("Found a datatype")
                        item['datatype']=node2.getAttribute("datatype")
                        
                L3=node2.getElementsByTagName(item['type'])
                for node3 in L3:
                    value = ""
                    for node4 in node3.childNodes:
                        if node4.nodeType == Node.TEXT_NODE:
                            value += node4.data
                            item['value']=value
                binding[key1]=item
            mapping.append(binding) 
            
        if output:
            try:
                outputfile = ''.join(['results/', output, ".py"])
                logger.debug("writing dictionary to file = [%s]\n" % outputfile)
                a = open(outputfile, 'w')
                pprint(mapping,a) 
            except IOError as (errno, strerror):
                logger.error("I/O error({0}): {1}".format(errno, strerror))
                logger.error("Failed to open query output file [%s]\n" % outputfile)
                return  
        logger.debug("result size = [%s]\n" % len(mapping))
        return mapping
