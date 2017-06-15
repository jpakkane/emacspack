#!/usr/bin/env python3

import sys, os, subprocess, shutil, uuid
import urllib.request

xml_templ = '''<?xml version='1.0' encoding='windows-1252'?>
<Wix xmlns='http://schemas.microsoft.com/wix/2006/wi'>
  <Product Name='GNU Emacs' Manufacturer='Free Software Foundation'
           Id='7312D310-673C-4BDF-BFF2-88273847D3AE' 
           UpgradeCode='2B2D1E25-946B-45F0-BB0F-32779C939B58'
           Language='1033' Codepage='1252' Version='%s'>
    <Package Id='*' Keywords='Installer' Description="Gnu Emacs %s Installer"
             Comments='Emacs is part of the GNU project.' Manufacturer='Free Software Foundation'
             InstallerVersion='100' Languages='1033' Compressed='yes' SummaryCodepage='1252' />

    <Media Id="1" Cabinet="emacs.cab" EmbedCab="yes" />

    <Feature Id='EmacsFeature' Level='1'>
      <ComponentGroupRef Id="EmacsGroup" />
    </Feature>

  </Product>
  <Fragment>
    <Directory Id='TARGETDIR' Name='SourceDir'>
      <Directory Id="ProgramFilesFolder">
	<Directory Id="fsfdir" Name="Free Software Foundation">
          <Directory Id="INSTALLDIR" Name="GNU Emacs">
	  </Directory>
	</Directory>
      </Directory>
    </Directory>
  </Fragment>
</Wix>
'''

def gen_guid():
    return str(uuid.uuid4()).upper()

class PackageGenerator:

    def __init__(self):
        self.version = '25.1'
        urlbase = 'http://ftp.gnu.org/gnu/emacs/windows/emacs-%s-i686-w64-mingw32.zip'
        self.url = urlbase % self.version
        self.fname = os.path.split(self.url)[-1]
        self.unpackdir = 'unpack'
        self.guid = '7312D310-673C-4BDF-BFF2-88273847D3AE'
        self.update_guid = '2B2D1E25-946B-45F0-BB0F-32779C939B58'
        self.harvested = 'EmacsGroup.wxs'
        self.main_xml = 'Emacs.wxs'
        self.final_output = 'emacs-%s.msi' % self.version
        self.dirs = ['bin', 'libexec', 'share', 'var']

    def generate(self):
        if not os.path.exists(self.fname):
            print('Downloading', self.url)
            urllib.request.urlretrieve(self.url, self.fname)
        if os.path.exists(self.unpackdir):
            shutil.rmtree(self.unpackdir)
        print('Unpacking archive')
        shutil.unpack_archive(self.fname, self.unpackdir)
        subprocess.check_call(['c:\\Program Files\\WiX Toolset v3.11\\bin\\heat.exe', 'dir', '.', '-gg', '-cg', 'EmacsGroup', '-dr', 'INSTALLDIR', '-out', self.harvested], cwd=self.unpackdir)
        with open(os.path.join(self.unpackdir, self.main_xml), 'w') as ofile:
            ofile.write(xml_templ % (self.version, self.version))
        subprocess.check_call(['c:\\Program Files\\WiX Toolset v3.11\\bin\\candle.exe', self.main_xml, '-o', '1.wixobj'], cwd=self.unpackdir)
        subprocess.check_call(['c:\\Program Files\\WiX Toolset v3.11\\bin\\candle.exe', self.harvested, '-o', '2.wixobj'], cwd=self.unpackdir)
        subprocess.check_call(['c:\\Program Files\\WiX Toolset v3.11\\bin\\light.exe', '1.wixobj', '2.wixobj', '-o', self.final_output], cwd=self.unpackdir)
        

if __name__ == '__main__':
    p = PackageGenerator()
    p.generate()
