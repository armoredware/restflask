    return jsonify({'user_id': page_details[0].user_id, 'last_mod':page_details[0].last_mod, 'timestamp':page_details[0].timestamp, 'domain':page_details[0].domain,
                   'url':page_details[0].url,
                   'xss':page_details[0].xss,
                   'sqli':page_details[0].sqli,
                   'sql':page_details[0].sql,
                   'csrf':page_details[0].csrf,
                   'hash':page_details[0].hash,
                   'uptime':page_details[0].uptime,
                   'loadspeed':page_details[0].loadspeed,
                   'pagecontent':page_details[0].pagecontent,
                   'externallinks':page_details[0].externallinks,
                   'scripts':page_details[0].scripts,
                   'base64':page_details[0].base64,
                   'documenttype':page_details[0].documenttype,
                   'virus':page_details[0].virus,
                   'malware':page_details[0].malware,
                   'reputation':page_details[0].reputation,
                   'popups':page_details[0].popups,
                   'bruteforce':page_details[0].bruteforce,
                   'title':page_details[0].title,
                   'redirect':page_details[0].redirect,
                   'sensitivedata':page_details[0].sensitivedata,
                   'emailaddresses':page_details[0].emailaddresses,
                   'adaissues':page_details[0].adaissues,
                   'accesscontrol':page_details[0].accesscontrol,
                   'vulnerability':page_details[0].vulnerability,
                   'scanned':page_details[0].scanned})
