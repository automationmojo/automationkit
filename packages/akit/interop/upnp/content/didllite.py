from typing import List, NamedTuple, Optional

from enum import Enum

from xml.etree.ElementTree import fromstring as from_xml_string
from xml.etree.ElementTree import Element

from akit.exceptions import AKitRuntimeError

DIDL_LINESEP = "\n"

DIDL_NAMESPACES = {
    "": "urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "r": "urn:schemas-rinconnetworks-com:metadata-1-0/",
    "upnp": "urn:schemas-upnp-org:metadata-1-0/upnp/"
}

class DidlDesc:

    def __init__(self, *, desc: str, **attrs):
        self._desc = desc
        self._attrs = attrs
        return

    def to_xml_lines(self, indent=""):

        xlines = [
            "{}<desc{}>".format(indent),
            "{}    {}".format(indent, self._desc),
            "{}</desc>".format(indent)
        ]

        return xlines
    
    def to_xml(self):

        attrs_str = ""

        attr_items = self._attrs.items()
        if len(attr_items) > 0:
            for ak, av in self._attrs.items():
                attrs_str = "{} {}='{}' ".format(attrs_str, ak, av)

        xstr = "<desc{}>{}</desc>".format(attrs_str, self._desc)

        return xstr

class DidlResource(NamedTuple):
    protocol_info: str
    uri: str
    duration: Optional[str] = None
    size: Optional[int] = None

    @classmethod
    def from_xml(cls, res_element: Element):
        return

    def to_xml_lines(self, indent=""):

        sizeattr = ""
        if self.size is not None:
            sizeattr = " size='{}'"

        xlines = [
            "{}<res protocolInfo='{}'{}>".format(indent, self.protocol_info, sizeattr),
            "{}    {}".format(indent, self.uri),
            "{}</res>".format(indent)
        ]

        return xlines

    def to_xml(self):
        
        sizeattr = ""
        if self.size is not None:
            sizeattr = " size='{}'"
        
        xstr = "<res protocolInfo='{}'{}>{}</res>".format(
            self.protocol_info, sizeattr, self.uri)

        return xstr

class DidlWriteStatus(str, Enum):
    MIXED = "MIXED"
    NOT_WRITABLE = "NOT_WRITABLE"
    PROTECTED = "PROTECTED"
    UNKNOWN = "UNKNOWN"
    WRITABLE = "WRITABLE"

class DidlObject:

    element_tag = None
    upnp_class = None

    def __init__(self, *, oid: str, parent_id: str, restricted: bool, title: str, res: DidlResource):
        self._oid = oid
        self._parent_id = parent_id
        self._restricted = restricted
        self._title = title
        self._res = res
        return

    @property
    def oid(self) -> str:
        return self._oid
    
    @property
    def parent_id(self) -> str:
        return self._parent_id
    
    @property
    def restricted(self) -> bool:
        return self._restricted

    @property
    def res(self) -> DidlResource:
        return self._res

    @property
    def title(self) -> str:
        return self._title

    def create_opening_element(self):
        estr = "<{} id='{}' parentID='{}' restricted='{}' >".format(
            self.element_tag, self._oid, self._parent_id, self._restricted)
        return estr
    
    def create_closing_element(self):
        estr = "</{}>".format(self.element_tag)
        return estr

    def to_xml_lines(self, indent=""):

        xlines = [
            self.create_opening_element()
        ]

        if self._title is not None:
            xlines.append('<dc:title>{}</dc:title>'.format(self._title))

        if self.upnp_class is not None:
            xlines.append('<upnp:class>{}</upnp:class>'.format(self.upnp_class))

        if self._res is not None:
            res_lines = self._res.to_xml_lines()
            xlines.extend(res_lines)

        xlines.append(self.create_closing_element())

        return xlines

    def to_xml(self):

        xml_parts = [
            self.create_opening_element()
        ]

        if self._title is not None:
            xml_parts.append('<dc:title>{}</dc:title>'.format(self._title))

        if self.upnp_class is not None:
            xml_parts.append('<upnp:class>{}</upnp:class>'.format(self.upnp_class))

        if self._res is not None:
            xml_parts.append(self._res.to_xml())

        xml_parts.append(self.create_closing_element())

        xmlstr = "".join(xml_parts)

        return xmlstr

class DidlContainerPhotoAlbum(DidlObject):

    element_tag = "container"
    upnp_class = "object.container.album.photoAlbum"

    def __init__(self, *, oid: str, parent_id: str, restricted: bool, title:str, child_count: int,
                 storage_used: int, write_status: str = DidlWriteStatus.UNKNOWN):
        super().__init__(oid=oid, parent_id=parent_id, restricted=restricted, title=title)
        self._child_count = child_count
        self._storage_used = storage_used
        self._write_status = write_status
        return
    
    @classmethod
    def from_xml(cls, obj_element: Element, namespaces: Optional[dict]=None):
        
        oid = obj_element.attrib["id"]
        parent_id = obj_element.attrib["parentID"]
        restricted = obj_element.attrib["restricted"]

        # Read the Required elements
        e_title = obj_element.find("dc:title", namespaces=namespaces)
        if e_title is None:
            errmsg = "DIDL message for DidlItemMusicTrack is missing a required element 'title'."
            raise AKitRuntimeError(errmsg)
        title = e_title.text

        obj = DidlContainerStorageFolder(oid=oid, parent_id=parent_id, restricted=restricted)
        return obj


class DidlContainerStorageFolder(DidlObject):

    element_tag = "container"
    upnp_class = "object.container.storageFolder"

    def __init__(self, *, oid: str, parent_id: str, restricted: bool, title:str, child_count: int,
                 storage_used: int, write_status: str = DidlWriteStatus.UNKNOWN):
        super().__init__(oid=oid, parent_id=parent_id, restricted=restricted, title=title)
        self._child_count = child_count
        self._storage_used = storage_used
        self._write_status = write_status
        return
    
    @classmethod
    def from_xml(cls, obj_element: Element, namespaces: Optional[dict]=None):
        
        oid = obj_element.attrib["id"]
        parent_id = obj_element.attrib["parentID"]
        restricted = obj_element.attrib["restricted"]

        # Read the Required elements
        e_title = obj_element.find("dc:title", namespaces=namespaces)
        if e_title is None:
            errmsg = "DIDL message for DidlItemMusicTrack is missing a required element 'title'."
            raise AKitRuntimeError(errmsg)
        title = e_title.text

        child_count = -1
        storage_used = -1
        write_status = DidlWriteStatus.UNKNOWN

        obj = DidlContainerStorageFolder(oid=oid, parent_id=parent_id, restricted=restricted, title=title,
            child_count=child_count, storage_used=storage_used, write_status=write_status)
        return obj


class DidlItemAlbumArt(DidlObject):

    element_tag = "item"
    upnp_class = "object.item.imageItem.photo.vendorAlbumArt"

    def __init__(self, *, oid: str, parent_id: str, restricted: bool, title:str, res: DidlResource):
        super().__init__(oid=oid, parent_id=parent_id, restricted=restricted, title=title, res=res)
        return

    @classmethod
    def from_xml(cls, obj_element: Element, namespaces: Optional[dict]=None):
        
        # Read the Required attributes
        oid = obj_element.attrib["id"]
        parent_id = obj_element.attrib["parentID"]
        restricted = obj_element.attrib["restricted"]

        obj = None
        return obj

class DidlItemMusicTrack(DidlObject):

    element_tag = "item"
    upnp_class = "object.item.audioItem.musicTrack"

    def __init__(self, *, oid: str, parent_id: str, restricted: bool, title: str, res: DidlResource, creator: str,
                 album_art: Optional[str] = None, genre: Optional[str] = None):
        super().__init__(oid=oid, parent_id=parent_id, restricted=restricted, title=title, res=res)
        self._creator = creator
        self._album_art = album_art
        self._genre = genre
        return
    
    @classmethod
    def from_xml(self, obj_element: Element, namespaces: Optional[dict]=None):

        # Read the Required attributes
        oid = obj_element.attrib["id"]
        parent_id = obj_element.attrib["parentID"]
        restricted = obj_element.attrib["restricted"]

        # Read the Required elements
        e_title = obj_element.find("dc:title", namespaces=namespaces)
        if e_title is None:
            errmsg = "DIDL message for DidlItemMusicTrack is missing a required element 'title'."
            raise AKitRuntimeError(errmsg)
        title = e_title.text

        e_res = obj_element.find("", namespaces=namespaces)
        if e_res is None:
            errmsg = "DIDL message for DidlItemMusicTrack is missing a required element 'title'."
            raise AKitRuntimeError(errmsg)
        res = DidlResource.from_xml(e_res)

        # Read the Optional elements
        creator = None
        e_creator = obj_element.find("dc:creator", namespaces=namespaces)
        if e_creator is not None:
            creator = e_creator.text

        album_art = None
        e_album_art = obj_element.find("upnp:albumArtURI", namespaces=namespaces)
        if e_album_art is not None:
            album_art = e_album_art.text

        obj = DidlItemMusicTrack(oid=oid, parent_id=parent_id, restricted=restricted, title=title, creator=creator, album_art=album_art)

        return obj


class DidlItemPhoto(DidlObject):

    element_tag = "item"
    upnp_class = "object.item.imageItem.photo"

    def __init__(self, *, oid: str, parent_id: str, restricted: bool, title:str, res: DidlResource, date: str):
        super().__init__(oid=oid, parent_id=parent_id, restricted=restricted, title=title, res=res)
        self._date = date
        return

    @property
    def date(self):
        return self._date
    
    @classmethod
    def from_xml(self, obj_element: Element, namespaces: Optional[dict]=None):
        
        # Read the Required attributes
        oid = obj_element.attrib["id"]
        parent_id = obj_element.attrib["parentID"]
        restricted = obj_element.attrib["restricted"]

        obj = None
        return obj


class DidlLitePacket:

    xml_namespaces = {
        'dc': 'http://purl.org/dc/elements/1.1/',
        'upnp': 'urn:schemas-upnp-org:metadata-1-0/upnp/',
        '': 'urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/'
    }

    def __init__(self, objects: List[DidlObject] = []):
        self._objects = objects
        return

    @property
    def objects(self):
        return self._objects

    def to_xml_lines(self, indent=""):

        attrs_str = ""
        for ak, av in self.xml_namespaces.items():
            "{} {}='{}' ".format(attrs_str, ak, av)

        xlines = [
            "<DIDL-Lite{}>".format(attrs_str)
        ]

        for obj in self._objects:
            obj_lines = obj.to_xml_lines(indent + "    ")
            xlines.extend(obj_lines)

        xlines.append("</DIDL-Lite>")

        return xlines

    def to_xml(self):

        attrs_str = ""
        for ak, av in self.xml_namespaces.items():
            "{} {}='{}' ".format(attrs_str, ak, av)

        xparts = [
            "<DIDL-Lite{}>".format(attrs_str)
        ]

        for obj in self._objects:
            xstr = obj.to_xml()
            xparts.append(xstr)

        xparts.append("</DIDL-Lite>")

        xstr = DIDL_LINESEP.join(xparts)

        return xstr

def parse_didl_lite_packet(content, namespaces=DIDL_NAMESPACES):

    root_element = from_xml_string(content)

    obj_items = []

    for obj_element in root_element.getchildren():
        
        class_element = obj_element.find("upnp:class", namespaces=namespaces)
        didl_class = class_element.text

        obj = None

        if didl_class == "object.container.storageFolder":
            obj = DidlContainerStorageFolder.from_xml(obj_element, namespaces=namespaces)
        elif didl_class == "object.item.imageItem.photo.vendorAlbumArt":
            obj = DidlItemAlbumArt.from_xml(obj_element, namespaces=namespaces)
        elif didl_class == "object.item.audioItem.musicTrack":
            obj = DidlItemMusicTrack.from_xml(obj_element, namespaces=namespaces)
        elif didl_class == "object.item.imageItem.photo":
            obj = DidlItemPhoto.from_xml(obj_element, namespaces=namespaces)
        else:
            errmsg = "Unknown DIDL object class '{}':".format(didl_class)
            raise AKitRuntimeError(errmsg)

        obj_items.append(obj)

    return

parse_didl_lite_packet("""
<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/"
           xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/"
           xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/"
           xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">
    <container id="13" parentID="2" restricted="0" searchable="1">
        <dc:title>Christmas</dc:title>
        <upnp:class>object.container.album.photoAlbum</upnp:class>
        <upnp:searchClass includeDerived="0">
            object.item.imageItem.photo
        </upnp:searchClass>
        <upnp:createClass includeDerived="0">
            object.item.imageItem.photo
        </upnp:createClass>
    </container>
    <container id="1" parentID="0" childCount="2" restricted="0">
        <dc:title>My Music</dc:title>
        <upnp:class>object.container.storageFolder</upnp:class>
        <upnp:storageUsed>730000</upnp:storageUsed>
        <upnp:writeStatus>WRITABLE</upnp:writeStatus>
        <upnp:searchClass includeDerived="0">
            object.container.album.musicAlbum
        </upnp:searchClass>
        <upnp:searchClass includeDerived="0">
            object.item.audioItem.musicTrack
        </upnp:searchClass>
        <upnp:createClass includeDerived="0">
            object.container.album.musicAlbum
        </upnp:createClass>
    </container> 
    <item id="-1" parentID="-1" restricted="true">
        <res protocolInfo="sonos.com-spotify:*:audio/x-spotify:*" duration="0:03:13">x-sonos-spotify:spotify%3atrack%3a7HXBG0W8gFJwHUh5mVF9tf?sid=9&amp;flags=8224&amp;sn=2</res>
        <r:streamContent></r:streamContent>
        <upnp:albumArtURI>/getaa?s=1&amp;u=x-sonos-spotify%3aspotify%253atrack%253a7HXBG0W8gFJwHUh5mVF9tf%3fsid%3d9%26flags%3d8224%26sn%3d2</upnp:albumArtURI>
        <dc:title>Rise</dc:title>
        <upnp:class>object.item.audioItem.musicTrack</upnp:class>
        <dc:creator>Lost Frequencies</dc:creator>
        <upnp:album>Rise</upnp:album>
    </item>
    <item id="31" parentID="30" restricted="0">
        <dc:title>Brand New Day</dc:title>
        <upnp:class name="Vendor Album Art">
            object.item.imageItem.photo.vendorAlbumArt
        </upnp:class>
        <res protocolInfo="http-get:*:image/jpeg:*" size="20000">
            http://10.0.0.1/getcontent.asp?id=31
        </res>
    </item> 
    <item id="14" parentID="12" restricted="0">
        <dc:title>Sunset on the beach</dc:title>
        <dc:date>2001-10-20</dc:date>
        <upnp:class>object.item.imageItem.photo</upnp:class>
        <res protocolInfo="http-get:*:image/jpeg:*" size="20000">
            http://10.0.0.1/getcontent.asp?id=14
        </res>
    </item> 
</DIDL-Lite>
""")