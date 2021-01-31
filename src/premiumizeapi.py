import logging
import requests
from src.model import *


class PremiumizeApi:

    def __init__(self, apikey, logger=None):

        self.apikey = apikey
        self.url = "https://www.premiumize.me/api"

        # Set up logger
        if not logger:
            self.log = logging.getLogger(self.__class__.__name__)
            self.log.propagate = 0
            self.log.setLevel(logging.DEBUG)
            screen_handler = logging.StreamHandler()
            screen_handler.setLevel(logging.DEBUG)
            self.log.addHandler(screen_handler)
            self.log.info("Created new logger since no logger was provided")
        else:
            self.log = logger
            self.log.debug("Using given logger")

    # ---- Networking --------------------------------------------------------------------

    def request(self, endpoint, params=None):
        """
        Makes a request to the Premiumize api
        :param endpoint:
        :param params:
        :return: The response to the request or None if something went wrong
        """

        path = self.url + endpoint

        # In case no params are given you better instantiate
        if params is None:
            params = {}

        self.log.debug("Sending request to " + path + " with params " + str(params))

        # Add api key
        params["apikey"] = self.apikey

        # And fly
        return requests.get(path, params=params)

    # ---- Folder -----------------------------------------------------------------------

    def folder_list(self, id, include_breadcrumbs=False):
        """
        List a folder.
        :param id: Id of the folder to be listed
        :param include_breadcrumbs: Breadcrumbs of the folder to be listed
        :return: Response or error
        """
        params = [("id", id), ("includebreadcrumbs", include_breadcrumbs)]
        logging.info("Requesting folder list with parameters: " + str(params))
        return request_get(folder_url + "list", create_payload(params))

    def folder_create(self, name, parent_id=None):
        """
        Create a new folder
        :param name: Name of the folder to be created
        :param parent_id: Optional id of the parent folder
        :return: ApiResponse or None
        """
        params = [("name", name)]
        if parent_id:
            params.append(parent_id)
        else:
            params.append(get_root_folder_id())
        logging.info("Requesting creation of folder with parameters: " + str(params))
        return request_get(folder_url + "create", create_payload(params))

    def folder_rename(self, id, name):
        """
        Rename a folder
        :param id: Id to be renamed
        :param name: New name
        :return: ApiResponse or None
        """
        params = [("id", id), ("name", name)]
        logging.info("Requesting renaming of folder with parameters: " + str(params))
        return request_get(folder_url + "rename", create_payload(params))

    # TODO implement
    def folder_paste(self, ids, types, id):
        """
        Paste multiple files or folders into a folder
        :param ids: Array of item id to be paste
        :param types: Array of the type to be paste. One of item_type_enum
        :param id: Id of folder to paste into
        :return: ApiResponse or None
        """
        return None

    def folder_delete(self, id):
        """
        Delete a folder
        :param id: Id of the folder to delete
        :return: ApiResponse or None
        """
        params = [("id", id)]
        logging.info("Requesting delete of folder with parameters: " + str(params))
        return request_get(folder_url + "delete", create_payload(params))

    # TODO implement
    def folder_uploadinfo(self, id):
        """
        get upload info. you will receive a token and a url. make a html upload to the url
        and send the file as "file" parameter and the token as "token" parameter.
        the file will be stored to the folder specified.
        :param id: Id of the folder
        :return: To be defined
        """
        return None

    def folder_search(self, name):
        """
        Search a folder or files
        :param name: The string to search for
        :return: A lot or None
        """
        params = [("q", name)]
        logging.info("Requesting search of folder with parameters: " + str(params))
        return request_get(folder_url + "search", create_payload(params))

    # ---- Item -----------------------------------------------------------------------

    def item_listall(self):
        """
        List all files
        :return: Array
        """
        return self.request(self.url + "/item/listall")

    def item_delete(self, id):
        """
        Delete an item
        :param id: Id of item to be deleted
        :return: ApiResponse
        """
        params = [("id", id)]
        return request_get(item_url + "delete", create_payload(params))

    def item_rename(self, id, name):
        """
        Rename an item
        :param id: Id of the item
        :param name: New name
        :return: ApiResponse
        """
        params = [("id", id), ("name", name)]
        return request_get(item_url + "rename", create_payload(params))

    def item_details(self, id):
        """
        Show details of an item
        :param id: Id of the item
        :return: A lot of information
        """
        return request_get(item_url + "details", create_payload([("id", id)]))

    # ---- Transfer -----------------------------------------------------------------------

    def transfer_create(self, magnet=None, torrent=None, folder_id=None):
        """
        Create a transfer. If no folder_id is given, the root folder is selected.

        :param magnet: src can be: http(s) links to supported container files, links to any supported website and magnet links.
        :param torrent: file (supported containerfiles, nzb, dlc)
        :param folder_id: Id of the target folder or None if root folder
        :return: {status, id, name, type} or None
        """

        # Check for input torrent information
        if not magnet and not torrent:
            raise ApiRequestError("One of magnet or torrent must be passed to create transfer!")
        elif magnet and torrent:
            raise ApiRequestError("You cannot pass magnet and torrent file at the same time!")

        # Check if a folder was given
        if not folder_id:
            folder_id = self.get_root_folder_id()

        if exit_flag:
            return None

        params = []
        if magnet:
            params.append(("folder_id", folder_id))
            params.append(("src", magnet))
            return request_get(transfer_url + "create", create_payload(params))
        if torrent:
            params.append(("folder_id", folder_id))
            return request_post(transfer_url + "create", create_payload(params), torrent)
        return None

    # TODO implement
    def transfer_directdl(self, src=None):
        """
        Create a direct download link.
        Note: This method contains redundant reponse data. The field 'content' contains a list of files,
                in case the requested data has more than 1 file (directories). If the response contains only
                one file, then the array will contain only one item. So as an app developer you can always use
                the content-arra and ignore the other fields. The other fields are there for legacy purposes.
                The fields location, filename, filesize will always contain the information for one file only.
        :param src: can be: http(s) links to cached container files, magnets and links to any supported websites.
        :return:
        """
        return None

    def transfer_list(self):
        """
        Get your transfers as a list
        :return: A list of transfers or None if something went wrong
        """
        return self.request(endpoint="/transfer/list")

    def transfer_clearfinished(self):
        """
        Clear finished transfers
        :return: ApiResponse or None
        """
        return self.request(endpoint="/transfer/clearfinished")

    def transfer_delete(self, id):
        """
        Delete a transfer
        :param id: Id of the transfer
        :return: ApiResponse
        """
        return self.request(endpoint="/transfer/delete", params={"id": id})

    # ---- Account -----------------------------------------------------------------------

    def account_info(self):
        """
        Get account info to apikey
        :return: Account information or None
        """
        # TODO add models and return them here!
        return self.request(endpoint="/account/info")

    # ---- Zip -----------------------------------------------------------------------

    # TODO implement
    def zip_generate(self, files=None, folder=None):
        """
        Generate a zip of files or folder. Can be mixed.
        :param files: Array of file ids to add to zip
        :param folder: Array of folder ids to add to zip
        :return: {status, location} or None
        """
        return None

    # ---- Cache -----------------------------------------------------------------------

    # TODO implement
    def cache_check(self, items):
        """
        Check supported links availability
        :param items: Array of items to be checked
        :return:
        """
        return None

    # ---- Services -----------------------------------------------------------------------

    def services_list(self):
        """
        Get a list of services information
        :return:
        """
        return self.request(endpoint="/services/list")

    # ---- Extras -----------------------------------------------------------------------

    def get_root_folder_id(self):
        """
        Finds the id of the root folder in premiumize cloud
        :return: The id of the root folder as string or None if not possible
        """
        # TODO implement
        items = self.item_listall().json()
        items = self.item_listall().files
        if len(items) == 0:
            logging.warning("Cannot get root folder id since no items could be found in the cloud")
            return None
        random_item_id = items[0].id
        response = self.item_details(random_item_id)
        random_folder_id = response.folder_id
        response = self.folder_list(random_folder_id, True)
        for breadcrumb in response.breadcrumbs:
            if breadcrumb.name == "My Files":
                return breadcrumb.id
        return None


api = PremiumizeApi("")
print(api.account_info().json())
