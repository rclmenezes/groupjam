import re
from django import forms
from django.forms.fields import ImageField
from django.contrib.auth.models import User

class RegisterEmailField(forms.EmailField):
    def clean(self, value):
        invalid_emails = ["fastmail.","freemail.","gmail.","lycosmail.","tiscali.","live.","aol.","hotmail.","yahoo.","gmx.","lycos.","rr.","altavista.","googlemail.","excite.com","wans.net","aim.com","compuserve.com","earthlink.net","facebook.com","fastmail.com","inbox.com","mac.com","mailinator.com","mailinator.net","me.com","msn.com","verizonmail.com","bigfoot.com","rediffmail.com","dodo.com.au","iinet.com.au","internode.com.au","internode.on.net","optusnet.com.au","tpg.com.au","bigpond.com","bigpond.com.au","telstra.com","telstra.net","eftel.com","eftel.com.au","exetel.com.au","aon.at","chello.at","utanet.at","scarlet.be","telenet.be","126.com","21cn.com","263.com","263.net","263.net.cn","3126.com","56.com","eyou.com","foxmail.com","sogou.com","tom.com  ","vip.qq.com","vip.sina.com","yeah.net","netease.com","qq.com","sina.com","sina.com.cn","tdc.dk","telia.dk","carlo.fr","cegetel.fr","fnac.net","guideo.fr","life.com","mac.fr","mageos.com","waika9.com","laposte.net","bouygtel.fr","free.fr","orange.fr","sfr.fr","aliceadsl.fr","club-internet.fr","freesbee.fr","infonie.fr","libertysurf.fr","neuf.fr","nomade.fr","tele2.fr","wanadoo.fr","worldonline.fr","live.de","netcologne.de","online.de","t-online.de","arcor.de","freenet.de","web.de","1email.eu","computerdirekt.net","directbox.com","hurra.de","istmail.de","strato.de","tonline.de","unicum.de","mail.com","iolfree.ie","alice.it","email.it","fastwebnet.it","inwind.it","iol.it","libero.it","live.it","tin.it","tiscalinet.it","virgilio.it","auone-net.jp","inter7.jp","nifmail.jp","biglobe.ne.jp","docomo.ne.jp","ezweb.ne.jp","vodafone.ne.jp","7chanmail","auone.jp","infoseek.jp","mail.goo.ne.jp","smoug.net","hanmail.net","nate.com","naver.com","CSWNet.com","12move.nl","casema.nl","chello.nl","freeler.nl","hetnet.nl","home.nl","kpnplanet.nl","live.nl","orange.nl","planet.nl","quicknet.nl","tele2.nl","versatel.nl","wanadoo.nl","worldonline.nl","wxs.nl","xs4all.nl","zeelandnet.nl","ziggo.nl","zonnet.nl","Clear.net.nz","Orcon.co.nz","Orcon.net.nz","Slingshot.co.nz","Vodafone.co.nz","Woosh.co.nz","Xtra.co.nz","terra.es","wanadoo.es","orange.es","superbanda.es","tele2.es","telecable.es","telefonica.net","vodafone.es","bluewin.ch","freesurf.ch","hispeed.ch","blueyonder.co.uk","live.co.uk","smartemail.co.uk","zzom.co.uk","btclick.com","btinternet.com","clara.net","freeserve.co.uk","teesdaleonline.co.uk","virgin.net","btopenworld.co.uk","googlemail.co.uk","googlemail.com","sky.co.uk","ask.co.uk","juno.com","alltel.net","ameritech.net","att.net","bellsouth.net","best.com","centurylink.net","covad.com","covad.net","embarqmail.com","flash.net","net.com","netzero.com","optimum.net","pacbell.net","prodigy.net","qwest.net","rocketmail.com","sbc.com","sbc.net","sbcglobal.net","snet.net","swbell.net","ymail.com","youreach.com","cablevision.net","centurytel.net","charter.net","clear.net","gci.net","hughesnet.com","insightbb.com","localnet.com","mchsi.com","unitedonline.net","comcast.net","verizon.net","dion.ne.jp"]
        
        super(RegisterEmailField, self).clean(value)
        
        domain = value.split('@')[1]
        for invalid in invalid_emails:
            if re.match(invalid, domain):
                raise forms.ValidationError("This looks like a personal email domain. Please use your work email.")
                
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("This email is already registered. Use the 'forgot password' link on the login page")
        except User.DoesNotExist:
            return value
    
class ConfirmationCodeField(forms.CharField):
    def clean(self, value):
        super(ConfirmationCodeField, self).clean(value)

        if len(value) != 15:
            raise forms.ValidationError("Invalid format. Are you sure you copied it correctly?")

        return value