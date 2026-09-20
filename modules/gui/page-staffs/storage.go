/* For license and copyright information please see the LEGAL file in the code repository */

package smp

import (
	error_p "memar/process/error/protocol"
	"memar/time/earth"

	storage_p "memar/storage/protocol"
	label_p "org/modules/knowledge/label/protocol"
	sp "org/modules/management/staff/protocol"
)

type StorageServices interface {
	LIST_StaffIDs_BY_Day(day earth.Day, offset, limit uint64) (staffIDs []sp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

	// we may need indexing based on mission type ??
	// FilterByType(t Type, offset, limit uint64) (staffIDs []sp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

	// FilterByStatus(status Status, offset, limit uint64) (staffIDs [][16]byte, nv storage_p.NumberOfVersion, err error_p.Error)

	FILTER_StaffIDs_BY_Reason(lID label_p.UUID, offset, limit uint64) (staffIDs []sp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

	FIND_StaffIDs_BY_EvaluatorIDs(evaluatorID sp.UUID, offset, limit uint64) (staffIDs []sp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	LIST_EvaluatorIDs_BY_StaffID(staffID sp.UUID, offset, limit uint64) (evaluatorIDs []sp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
