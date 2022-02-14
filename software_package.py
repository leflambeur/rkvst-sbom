# pylint:disable=missing-function-docstring      # docstrings
# pylint:disable=missing-module-docstring      # docstrings
# pylint:disable=missing-class-docstring      # docstrings

from typing import Optional

# pylint:disable=unused-import      # To prevent cyclical import errors forward referencing is used
# pylint:disable=cyclic-import      # but pylint doesn't understand this feature

from archivist import archivist as type_helper
import xml.etree.ElementTree as ET


class SoftwarePackage:
    def __init__(self, arch: "type_helper.Archivist"):
        self._arch = arch
        self._asset = None

    @property
    def arch(self):
        return self._arch

    @property
    def asset(self):
        return self._asset
    
    @property
    def attachments(self):
        return self._attachments

    # Asset Creation
    def create(
        self,
        attrs: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):
        self._add_attachments(attachments)

        attrs = {
            "arc_display_name": attrs['name'],
            "arc_description": attrs['description'],
            "arc_display_type": "Software Package",
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        self._asset = self.arch.assets.create(attrs=attrs, confirm=True)
        return self._asset

    # Asset load by unique identity
    def read(
        self,
        identity: str,
    ):
        self._asset = self.arch.assets.read(identity)

    # Asset load by attribute(s)
    def read_by_signature(
        self,
        attributes: Optional[dict],
    ):
        # Hard-wire the Asset type
        newattrs = attributes.copy()
        newattrs["arc_display_type"] = "Software Package"

        # Note: underlying Archivist will raise ArchivistNotFoundError or
        # ArchivistDuplicateError unless this set of attributes points to
        # a single unique asset
        self._asset = self.arch.assets.read_by_signature(attrs=newattrs)

    # Release Events
    def release(
        self,
        attrs: dict,
        *,
        attachments: Optional[list] = None,
        latest_sbom: Optional[dict] = None,
        custom_attrs: Optional[dict] = None,
        custom_asset_attrs: Optional[dict] = None,
        refBom: Optional[bool],
    ):
        
        self._add_attachments(attachments)
        # sbom_name: str,
        # sbom_description: str,
        # sbom_hash: str,
        # sbom_version: str,
        # sbom_author: str,
        # sbom_supplier: str,
        # sbom_uuid: str,

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }

        if latest_sbom is None:
            latest_sbom = attrs
        attrs = {
            "arc_description": attrs["description"],
            "arc_evidence": "Release",
            "arc_display_type": "Release",
            "sbom_component": attrs["name"],
            "sbom_hash": attrs["hash"],
            "sbom_version": attrs["version"],
            "sbom_author": attrs["author"],
            "sbom_supplier": attrs["supplier"],
            "sbom_uuid": attrs["uuid"],
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        asset_attrs = {
            "arc_display_name": latest_sbom["name"],
            "sbom_component": latest_sbom["name"],
            "sbom_hash": latest_sbom["hash"],
            "sbom_version": latest_sbom["version"],
            "sbom_author": latest_sbom["author"],
            "sbom_supplier": latest_sbom["supplier"],
            "sbom_uuid": latest_sbom["uuid"],
        }
        if custom_asset_attrs is not None:
            asset_attrs.update(custom_asset_attrs)

        return self.arch.events.create(
            self.asset["identity"],
            props=props,
            attrs=attrs,
            asset_attrs=asset_attrs,
            confirm=True,
        )

    def release_plan(
        self,
        attrs: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):
        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": attrs["description"],
            "arc_evidence": "Release Plan",
            "arc_display_type": "Release Plan",
            "sbom_planned_date": attrs["date"],
            "sbom_planned_captain": attrs["captain"],
            "sbom_planned_component": attrs["name"],
            "sbom_planned_version": attrs["version"],
            "sbom_planned_reference": attrs["reference"],
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    def release_accepted(
        self,
        attrs: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):
        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": attrs["description"],
            "arc_evidence": "Release Accepted",
            "arc_display_type": "Release Accepted",
            "sbom_accepted_date": attrs["date"],
            "sbom_accepted_captain": attrs["captain"],
            "sbom_accepted_component": attrs["name"],
            "sbom_accepted_version": attrs["version"],
            "sbom_accepted_approver": attrs["approver"],
            "sbom_accepted_vuln_reference": attrs["reference"],
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    # Patch Events
    def patch(
        self,
        attrs: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):
        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": attrs["description"],
            "arc_evidence": "Patch",
            "arc_display_type": "Patch",
            "sbom_patch_component": attrs["target_component"],
            "sbom_patch_hash": attrs["hash"],
            "sbom_patch_target_version": attrs["target_version"],
            "sbom_patch_author": attrs["author"],
            "sbom_patch_supplier": attrs["supplier"],
            "sbom_patch_uuid": attrs["uuid"],
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    def private_patch(
        self,
        attrs: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):
        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": attrs["description"],
            "arc_evidence": attrs["private_id"] + "_Patch",
            "arc_display_type": attrs["private_id"] + "_Patch",
            "sbom_patch_component": attrs["target_component"],
            "sbom_patch_hash": attrs["hash"],
            "sbom_patch_version": attrs["target_version"],
            "sbom_patch_author": attrs["author"],
            "sbom_patch_supplier": attrs["supplier"],
            "sbom_patch_uuid": attrs["uuid"],
            "sbom_patch_vuln_reference": attrs["reference"],
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    # Vulnerability Events
    def vuln_disclosure(
        self,
        attrs: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict],
    ):
        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": attrs["description"],
            "arc_evidence": "Vulnerability Disclosure",
            "arc_display_type": "Vulnerability Disclosure",
            "vuln_name": attrs["name"],
            "vuln_reference": attrs["reference"],
            "vuln_id": attrs["id"],
            "vuln_category": attrs["category"],
            "vuln_severity": attrs["severity"],
            "vuln_status": attrs["status"],
            "vuln_author": attrs["author"],
            "vuln_target_component": attrs["target_component"],
            "vuln_target_version": attrs["target_version"],
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }

        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )

    def vuln_update(
        self,
        attrs: dict,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):
        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": attrs["description"],
            "arc_evidence": "Vulnerability Update",
            "arc_display_type": "Vulnerability Update",
            "vuln_name": attrs["name"],
            "vuln_reference": attrs["reference"],
            "vuln_id": attrs["id"],
            "vuln_category": attrs["category"],
            "vuln_severity": attrs["severity"],
            "vuln_status": attrs["status"],
            "vuln_author": attrs["author"],
            "vuln_target_component": attrs["target_component"],
            "vuln_target_version": attrs["target_version"],
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )
    
    def vuln_report(
        self,
        attrs: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
        ):

        self._add_attachments(attachments)

        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }
        attrs = {
            "arc_description": attrs["description"],
            "arc_evidence": "Vulnerability Report",
            "arc_display_type": "Vulnerability Report",
            "vuln_component": attrs["component"],
            "vuln_author": attrs["author"],
            "vuln_target_version": attrs["target_version"],
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )
    # EOL/Deprecation
    def deprecation(
        self,
        attrs: dict,
        *,
        attachments: Optional[list] = None,
        custom_attrs: Optional[dict] = None,
    ):
        self._add_attachments(attachments)
        
        props = {
            "operation": "Record",
            "behaviour": "RecordEvidence",
        }

        attrs = {
            "arc_description": attrs["description"],
            "arc_evidence": "Deprecation",
            "arc_display_type": "Deprecation",
            "sbom_eol_target_component": attrs["target_component"],
            "sbom_eol_target_version": attrs["target_version"],
            "sbom_eol_target_uuid": attrs["target_uuid"],
            "sbom_eol_target_date": attrs["target_date"],
            "arc_attachments": [
                {
                    "arc_display_name": attrs["description"],
                    "arc_attachment_identity": attachment["identity"],
                    "arc_hash_value": attachment["hash"]["value"],
                    "arc_hash_alg": attachment["hash"]["alg"],
                }
                for attachment in self._attachments
            ],
        }
        if custom_attrs is not None:
            attrs.update(custom_attrs)

        return self.arch.events.create(
            self._asset["identity"], props=props, attrs=attrs, confirm=True
        )
    
    def _add_attachments(self, attachments: list):
        self._attachments = []
        for attachment in attachments:
            with open(f"{attachment}", "rb") as fd:
                self._attachments.append(self.arch.attachments.upload(fd))
