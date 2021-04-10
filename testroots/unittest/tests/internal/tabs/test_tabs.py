
import os
import shutil

import akit.environment.activate # pylint: disable=unused-import

from akit.paths import get_path_for_artifacts
from akit.testing.unittest.testcontainer import PositiveTestContainer
from akit.testing.unittest.testpack import DefaultTestPack

from akit.templates import TABS_TEMPLATE_IMAGES, TABS_TEMPLATE_SOUNDS

DIR_PARENT = os.path.dirname(os.path.abspath(__file__))

DIR_SOUNDS = os.path.join(DIR_PARENT, "sounds")
DIR_IMAGES = os.path.join(DIR_PARENT, "images")


class TestArtifactTabs(PositiveTestContainer, DefaultTestPack):

    def test_tabs_images(self):
        artifact_dir = get_path_for_artifacts("images")

        for dir, folder_list, file_list in os.walk(DIR_IMAGES):
            for file in file_list:
                src_full = os.path.join(dir, file)
                dest_full = os.path.join(artifact_dir, file)
                shutil.copy2(src_full, dest_full)
        
        tab_page_full = os.path.join(artifact_dir, "tab.html")
        shutil.copy2(TABS_TEMPLATE_IMAGES, tab_page_full)
        return

    def test_tabs_sounds(self):
        artifact_dir = get_path_for_artifacts("sounds")

        for dir, folder_list, file_list in os.walk(DIR_SOUNDS):
            for file in file_list:
                src_full = os.path.join(dir, file)
                dest_full = os.path.join(artifact_dir, file)
                shutil.copy2(src_full, dest_full)
        
        tab_page_full = os.path.join(artifact_dir, "tab.html")
        shutil.copy2(TABS_TEMPLATE_SOUNDS, tab_page_full)
        return

if __name__ == "__main__":
    from akit.testing.unittest.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
