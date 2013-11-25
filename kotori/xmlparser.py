#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
import re
from gconf import GConf as gconf

def test(x):
    print x

def parseXML(xmlStr):
    return ET.fromstring(xmlStr).text

def verify_login(loginResStr):
    s = parseXML(loginResStr)
    if s.find(gconf.FORUM_URL) == -1:
        return False
    else:
        return True

def parse_rate_limit(rateFormStr):
    class RateLimParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.tdCnt = 0
            self.rateLim = None
        def handle_starttag(self, tag, attrs):
            if tag == 'td':
                self.tdCnt += 1
        
        def handle_data(self, data):
            if self.rateLim is None and self.tdCnt == 4: # magic number
                self.rateLim = int(data)
    s = parseXML(rateFormStr)
    p = RateLimParser()
    p.feed(s)
    return p.rateLim

# test case
if __name__ == '__main__':
    rfs = """<?xml version="1.0" encoding="utf-8"?>
<root><![CDATA[<div class="tm_c" id="floatlayout_topicadmin">
<h3 class="flb">
<em id="return_rate">评分</em>
<span>
<a href="javascript:;" class="flbc" onclick="hideWindow('rate')" title="关闭">关闭</a></span>
</h3>
<form id="rateform" method="post" autocomplete="off" action="forum.php?mod=misc&amp;action=rate&amp;ratesubmit=yes&amp;infloat=yes" onsubmit="ajaxpost('rateform', 'return_rate', 'return_rate', 'onerror');">
<input type="hidden" name="formhash" value="44492c28" />
<input type="hidden" name="tid" value="643316" />
<input type="hidden" name="pid" value="22412315" />
<input type="hidden" name="referer" value="http://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=643316&page=0#pid22412315" />
<input type="hidden" name="handlekey" value="rate"><div class="c">
<table cellspacing="0" cellpadding="0" class="dt mbm">
<tr>
<th>&nbsp;</th>
<th width="65">&nbsp;</th>
<th width="65">评分区间</th>
<th width="55">今日剩余</th>
</tr><tr>
<td> 战斗力</td>
<td>
<input type="text" name="score1" id="score1" class="px z" value="0" style="width: 25px;" />
<a href="javascript:;" class="dpbtn" onclick="showselect(this, 'score1', 'scoreoption1')">^</a>
<ul id="scoreoption1" style="display:none"><li>+1</li><li>-1</li></ul>
</td>
<td>-1 ~ 1</td><td>2</td>
</tr>
</table>

<div class="tpclg">
<h4>可选评分理由:</h4>
<table cellspacing="0" cellpadding="0" class="reason_slct"> 	<tr>
 		<td>
 			<ul id="reasonselect" class="reasonselect pt"><li>####乱玩评分 管理员扣你们9999鹅####</li><li>-------------------------------------------------</li><li>谢谢大大发片!!!</li><li>楼主纯福利</li><li>我要给风舞雪大大介绍妹子</li></ul>
 			<script type="text/javascript" reload="1">
 				var reasonSelectOption = $('reasonselect').getElementsByTagName('li');
 				if (reasonSelectOption) {
 					for (i=0; i<reasonSelectOption.length; i++) {
 						reasonSelectOption[i].onmouseover = function() { this.className = 'xi2 cur1'; }
 						reasonSelectOption[i].onmouseout = function() { this.className = ''; }
 						reasonSelectOption[i].onclick = function() {
 							$('reason').value = this.innerHTML;
 						}
 					}
 				}
 			</script>
 		</td>
 	</tr>
<tr>
 	 	<td><input type="text" name="reason" id="reason" class="px" onkeyup="seditor_ctlent(event, '$(\'rateform\').ratesubmit.click()')" /></td>
</tr>
</table>
</div>
</div>
<p class="o pns">
<label for="sendreasonpm"><input type="checkbox" name="sendreasonpm" id="sendreasonpm" class="pc" checked="checked" disabled="disabled" />通知作者</label>
<button name="ratesubmit" type="submit" value="true" class="pn pnc"><span>确定</span></button>
</p>
</form>
</div>


<script type="text/javascript" reload="1">
function succeedhandle_rate(locationhref) {
ajaxget('forum.php?mod=viewthread&tid=643316&viewpid=22412315', 'post_22412315', 'post_22412315');
hideWindow('rate');
}
loadcss('forum_moderator');
</script>

]]></root>"""
    print parse_rate_limit(rfs)
