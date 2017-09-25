import re

def RemoveCharacters(text):
    # This function removes some non-grammatical characters 
    # and add extra spaces to punctuations in order to facilitate 
    # spelling error correction.
    output = text
    output = output.replace('"','')
    output = output.replace('.', ' . ')
    output = output.replace(',', ' , ')
    output = output.replace('?', ' ? ')
    output = output.replace('(', ' ( ')
    output = output.replace(')', ' ) ')
    output = output.replace('$', ' $ ')
    output = output.replace(';',' ; ')
    output = output.replace('!',' ! ')
    output = output.replace('}','')
    output = output.replace('{','')
    output = output.replace('/',' ')
    output = output.replace('_',' ')
    output = output.replace('*','')
    return output

def CleanXML(text):
    # This function removes markups
    
    output = text #initialize output
    
    # '&amp;lt;/p&amp;gt;' and '&amp;lt;p&amp;gt;' are line-breaks
    NewlinePattern = re.compile( re.escape('&amp;lt;/p&amp;gt;') 
                                + '|' 
                                + re.escape('&amp;lt;p&amp;gt;') )
    
    output = re.sub(NewlinePattern,'\n',output)
    
    # replace all other markups

    XMLmarkups = ['name=&amp;quot;ValidationSchema&amp;quot;', 
                   'content=&amp;quot;', 
                   '&amp;quot;/&amp;gt;', 
                   '&amp;lt;meta']
    
    for pattern in XMLmarkups: 
        output = re.sub(re.escape(pattern),'',output , re.IGNORECASE)
        
    html_header = re.compile(re.escape('&amp;lt;') 
                             + '/?html/?' 
                             + re.escape('&amp;gt;'))
    
    output = re.sub(html_header,'',output)
    
    body_header = re.compile(re.escape('&amp;lt;') 
                             + '/?body/?' 
                             + re.escape('&amp;gt;'))
    
    output = re.sub(body_header,'',output)
    
    title_header = re.compile(re.escape('&amp;lt;') 
                              + '/?title/?' 
                              + re.escape('&amp;gt;'))
    
    output = re.sub(title_header,'',output)
    
    head_header = re.compile(re.escape('&amp;lt;') 
                             + '/?head/?' 
                             + re.escape('&amp;gt;'))
    
    output = re.sub(head_header,'',output)

    HTTPpattern = re.compile( re.escape('http://') + '\S*'  
                             + re.escape('.xsd') )

    output = re.sub(HTTPpattern,'',output)
    output = re.sub(re.escape('&amp;quot;'),'"',output)
    output = re.sub(re.escape('&amp;apos;'),"'",output)
    output = re.sub(re.escape('&amp;amp;'),"&",output)
    output = re.sub(re.escape('&amp'),'',output)
    output = re.sub(re.escape('&lt;'),'',output)
    output = re.sub(re.escape('&gt;'),'',output)
    output = RemoveCharacters(output)
        
    return ' '.join([w for w in re.split(' ',output) if not w==''])

def ExtractElement(text,field):
    # This function takes input string (text) and looks for markups.
    # input "field" is a specific element that the code looks for.
    # For example, the page title can be located in the text as:   
    # <recordtitle> Display Ad 33 -- No Title </recordtitle>
    # Here, "field" variable is "recordtitle".
    # (Note: all searches are not case-sensitive.)

    beginMarkup = '<' + field + '>' #example: <recordtitle> 
    endMarkup = '</' + field + '>' #example: </recordtitle>

    textNoLineBreak = re.sub(r'\n|\r\n','',text) #delete the line break

    # Windows and Linux use different line break ('\n' vs '\r\n')

    ElementPattern = re.compile( re.escape(beginMarkup) + '.*' + re.escape(endMarkup), re.IGNORECASE )
    ElementMarkup = re.compile( re.escape(beginMarkup) + '|' + re.escape(endMarkup), re.IGNORECASE)

    DetectElement = re.findall(ElementPattern,textNoLineBreak)
    
    #strip markup
    Content = str(re.sub(ElementMarkup,'',str(DetectElement[0]))) 
    
    #reset space
    Content = ' '.join([w for w in re.split(' ',Content) if not w=='']) 
    
    return Content

def AssignPageIdentifier(text, journal):
    # This function assigns page identifier.
    # For example, 'WSJ_classifiedad_19780912_45'.
    # 'WSJ' is the journal name, to be specified by the user.
    # 'classifiedad' means the page is Classified Ad.
    # '19780912' is the publication date.
    # '45' is the page number.
    
    recordtitle = ExtractElement(text,'recordtitle')
    
    # All classified ad pages have 'recordtitle' of 'Classified Ad [number] -- No Title'.
    # (likewise for display ad pages) 
    
    Match = re.findall('Ad \d+ -- No Title',recordtitle,re.IGNORECASE)
    
    if Match: # this page is either display ad or classified ad
        
        if re.findall('Display Ad',recordtitle,re.IGNORECASE):
            ad_type = 'displayad'
        elif re.findall('Classified Ad',recordtitle,re.IGNORECASE): 
            ad_type = 'classifiedad'
        
        ad_number = re.findall('\d+',recordtitle)[0] # get the page number
        
        numericpubdate = ExtractElement(text,'numericpubdate')
        pub_date = re.findall('\d{8}',numericpubdate)[0] # get the publication date
        
        output = '_'.join([journal,ad_type,pub_date,ad_number]) # create page identifider
    else:
        output = None
        
    return output

#...............................................#   



