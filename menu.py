
class Menu:
    """
    Class to create and manage a text-based menu.
    """
    def __init__(self):
        pass

    def create_menu(self, dynamic_options: list[str] = None,
                    static_options: list[str] = None) -> str:
        """
        Create a text-based menu with the given dynamic and static options.

        Args:
        dynamic_options (list[str]): List of dynamic options to be
        included in the menu.
        static_options (list[str]): List of static options to be
        included in the menu.

        Returns:
        str: Text-based menu string.
        """
        menu = '\n'
        menu_options = []

        if dynamic_options:
            for dynamic_option in dynamic_options:
                menu_options.append(dynamic_option)
        if static_options:
            for static_option in static_options:
                menu_options.append(static_option)

        option_index = 1
        for menu_option in menu_options:
            menu = menu + f'{option_index}. {menu_option}\n'
            option_index += 1

        return menu
    
    def get_choosed_menu_option(self, menu: str, choosed_option: str) -> str:
        """
        Get the chosen menu option based on user input.
        If option doesn't exist in provided option an empty string will be
        returned.

        Args:
        menu (str): Text-based menu string.
        choosed_option (str): User's chosen option.

        Returns:
        str: Chosen menu option.
        """
        if choosed_option in menu:
            user_input_menu_option_index = menu.find(choosed_option)
            choosed_option = (
                menu[user_input_menu_option_index+3:menu.find('\n',
                                                              user_input_menu_option_index)]
                                                              )
            return choosed_option
        else:
            return ''
    