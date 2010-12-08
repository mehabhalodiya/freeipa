# Authors:
#   Jr Aquino <jr.aquino@citrixonline.com>
#
# Copyright (C) 2010  Red Hat
# see file 'COPYING' for use and warranty information
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 only
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""
Sudo Rule
"""

from ipalib import api, errors
from ipalib import Str, StrEnum
from ipalib.plugins.baseldap import *
from ipalib import _, ngettext

class sudorule(LDAPObject):
    """
    Sudo Rule.
    """
    container_dn = api.env.container_sudorule
    object_name = 'Sudo Rule'
    object_name_plural = 'Sudo Rules'
    object_class = ['ipaassociation', 'ipasudorule']
    default_attributes = [
        'cn', 'ipaenabledflag',
        'description', 'usercategory', 'hostcategory',
        'cmdcategory', 'memberuser', 'memberhost',
        'memberallowcmd', 'memberdenycmd',
    ]
    uuid_attribute = 'ipauniqueid'
    rdn_attribute = 'ipauniqueid'
    attribute_members = {
        'memberuser': ['user', 'group'],
        'memberhost': ['host', 'hostgroup'],
        'memberallowcmd': ['sudocmd', 'sudocmdgroup'],
        'memberdenycmd': ['sudocmd', 'sudocmdgroup'],
    }

    label = _('SUDO')

    takes_params = (
        Str('cn',
            cli_name='sudorule_name',
            label=_('Rule name'),
            primary_key=True,
        ),
        Str('description?',
            cli_name='desc',
            label=_('Description'),
        ),
        Flag('ipaenabledflag?',
             label=_('Enabled'),
             flags=['no_create', 'no_update', 'no_search'],
        ),
        StrEnum('usercategory?',
            cli_name='usercat',
            label=_('User category'),
            doc=_('User category the rule applies to'),
            values=(u'all', ),
        ),
        StrEnum('hostcategory?',
            cli_name='hostcat',
            label=_('Host category'),
            doc=_('Host category the rule applies to'),
            values=(u'all', ),
        ),
        StrEnum('cmdcategory?',
            cli_name='cmdcat',
            label=_('Command category'),
            doc=_('Command category the rule applies to'),
            values=(u'all', ),
        ),
            Str('memberuser_user?',
            label=_('Users'),
            flags=['no_create', 'no_update', 'no_search'],
        ),
        Str('memberhost_host?',
            label=_('Hosts'),
            flags=['no_create', 'no_update', 'no_search'],
        ),
        Str('memberhost_hostgroup?',
            label=_('Host Groups'),
            flags=['no_create', 'no_update', 'no_search'],
        ),
        Str('memberallowcmd_sudocmd?',
            label=_('Sudo Allow Commands'),
            flags=['no_create', 'no_update', 'no_search'],
        ),
        Str('memberdenycmd_sudocmd?',
            label=_('Sudo Deny Commands'),
            flags=['no_create', 'no_update', 'no_search'],
        ),
        Str('memberallowcmd_sudocmdgroup?',
            label=_('Sudo Command Groups'),
            flags=['no_create', 'no_update', 'no_search'],
        ),
        Str('memberdenycmd_sudocmdgroup?',
            label=_('Sudo Command Groups'),
            flags=['no_create', 'no_update', 'no_search'],
        ),

    )

api.register(sudorule)


class sudorule_add(LDAPCreate):
    """
    Create new Sudo Rule.
    """
    def pre_callback(self, ldap, dn, entry_attrs, attrs_list, *keys, **options):
        # Sudo rules are enabled by default
        entry_attrs['ipaenabledflag'] = 'TRUE'
        return dn

    msg_summary = _('Added sudo rule "%(value)s"')

api.register(sudorule_add)


class sudorule_del(LDAPDelete):
    """
    Delete Sudo Rule.
    """

api.register(sudorule_del)


class sudorule_mod(LDAPUpdate):
    """
    Modify Sudo Rule.
    """

api.register(sudorule_mod)


class sudorule_find(LDAPSearch):
    """
    Search for Sudo Rule.
    """

api.register(sudorule_find)


class sudorule_show(LDAPRetrieve):
    """
    Dispaly Sudo Rule.
    """

api.register(sudorule_show)


class sudorule_enable(LDAPQuery):
    """
    Enable a Sudo rule.
    """
    def execute(self, cn):
        ldap = self.obj.backend

        dn = self.obj.get_dn(cn)
        entry_attrs = {'ipaenabledflag': 'TRUE'}

        try:
            ldap.update_entry(dn, entry_attrs)
        except errors.EmptyModlist:
            pass
        except errors.NotFound:
            self.obj.handle_not_found(cn)

        return dict(result=True)

    def output_for_cli(self, textui, result, cn):
        textui.print_name(self.name)
        textui.print_dashed('Enabled Sudo rule "%s".' % cn)

api.register(sudorule_enable)


class sudorule_disable(LDAPQuery):
    """
    Disable a Sudo rule.
    """
    def execute(self, cn):
        ldap = self.obj.backend

        dn = self.obj.get_dn(cn)
        entry_attrs = {'ipaenabledflag': 'FALSE'}

        try:
            ldap.update_entry(dn, entry_attrs)
        except errors.EmptyModlist:
            pass
        except errors.NotFound:
            self.obj.handle_not_found(cn)

        return dict(result=True)

    def output_for_cli(self, textui, result, cn):
        textui.print_name(self.name)
        textui.print_dashed('Disabled Sudo rule "%s".' % cn)

api.register(sudorule_disable)


class sudorule_add_allow_command(LDAPAddMember):
    """
    Add commands and sudo command groups affected by Sudo Rule.
    """
    member_attributes = ['memberallowcmd']
    member_count_out = ('%i object added.', '%i objects added.')

api.register(sudorule_add_allow_command)


class sudorule_remove_allow_command(LDAPRemoveMember):
    """
    Remove commands and sudo command groups affected by Sudo Rule.
    """
    member_attributes = ['memberallowcmd']
    member_count_out = ('%i object removed.', '%i objects removed.')

api.register(sudorule_remove_allow_command)


class sudorule_add_deny_command(LDAPAddMember):
    """
    Add commands and sudo command groups affected by Sudo Rule.
    """
    member_attributes = ['memberdenycmd']
    member_count_out = ('%i object added.', '%i objects added.')

api.register(sudorule_add_deny_command)


class sudorule_remove_deny_command(LDAPRemoveMember):
    """
    Remove commands and sudo command groups affected by Sudo Rule.
    """
    member_attributes = ['memberdenycmd']
    member_count_out = ('%i object removed.', '%i objects removed.')

api.register(sudorule_remove_deny_command)


class sudorule_add_user(LDAPAddMember):
    """
    Add users and groups affected by Sudo Rule.
    """
    member_attributes = ['memberuser']
    member_count_out = ('%i object added.', '%i objects added.')

api.register(sudorule_add_user)


class sudorule_remove_user(LDAPRemoveMember):
    """
    Remove users and groups affected by Sudo Rule.
    """
    member_attributes = ['memberuser']
    member_count_out = ('%i object removed.', '%i objects removed.')

api.register(sudorule_remove_user)


class sudorule_add_host(LDAPAddMember):
    """
    Add hosts and hostgroups affected by Sudo Rule.
    """
    member_attributes = ['memberhost']
    member_count_out = ('%i object added.', '%i objects added.')

api.register(sudorule_add_host)


class sudorule_remove_host(LDAPRemoveMember):
    """
    Remove hosts and hostgroups affected by Sudo Rule.
    """
    member_attributes = ['memberhost']
    member_count_out = ('%i object removed.', '%i objects removed.')

api.register(sudorule_remove_host)
