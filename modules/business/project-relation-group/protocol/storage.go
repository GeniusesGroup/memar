/* For license and copyright information please see the LEGAL file in the code repository */

package prgp

import (
	error_p "memar/error/protocol"

	pp "org/modules/business/project/protocol"
	gp "org/modules/organization/group/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(projectID pp.UUID, GroupID gp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(projectID pp.UUID, GroupID gp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	LIST_GroupIDs_BY_ProjectIDs(projectID pp.UUID, offset, limit uint64) (GroupIDs []gp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	LIST_ProjectIDs_BY_GroupID(GroupID gp.UUID, offset, limit uint64) (projectIDs []pp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
