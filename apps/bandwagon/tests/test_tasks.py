import os
import shutil
import tempfile

from django import test
from django.conf import settings

from nose.tools import eq_
from PIL import Image

from bandwagon.tasks import resize_icon

class TestTasks(test.TestCase):

    def test_resize_icon(self):
        somepic = "%s/img/amo2009/tab-mozilla.png" % settings.MEDIA_ROOT

        src = tempfile.NamedTemporaryFile(mode='r+w+b', suffix=".png",
                                          delete=False)
        dest = tempfile.NamedTemporaryFile(mode='r+w+b', suffix=".png")

        # resize_icon removes the original
        shutil.copyfile(somepic, src.name)

        src_image = Image.open(src.name)
        eq_(src_image.size, (82,31))

        resize_icon(src.name, dest.name)

        dest_image = Image.open(dest.name)
        eq_(dest_image.size, (32,12))

        assert not os.path.exists(src.name)
