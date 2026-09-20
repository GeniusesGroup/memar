/* For license and copyright information please see the LEGAL file in the code repository */

package graph_p

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	qp "org/modules/identity/thing/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(quiddityID qp.UUID, priority uint64) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(quiddityID qp.UUID, priority uint64, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	// Delete(ownerID org.UUID, departmentID dp.UUID) (err error_p.Error)

	ListQuiddities(complementID qp.UUID, offset, limit uint64) (quiddityIDs []qp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	ListPriorities(quiddityID, complementID qp.UUID, offset, limit uint64) (priorities []uint64, nv storage_p.NumberOfVersion, err error_p.Error)
}

// type StorageServices interface {
// 	Save(dm DataModel) (err error_p.Error)

// 	Get(quiddityID qp.UUID) (dm DataModel, err error_p.Error)

// 	FIND_BY_UserID(userID user_p.UUID, offset, limit uint64) (quiddityIDs []qp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

// 	// e.g. find user requests id in request module.
// 	// FIND_BY_UserID_AND_ModuleID

// 	// LIST_UserIDs_BY_CommentID(commentID cp.UUID, offset, limit uint64) (userIDs []user_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// }

// ListQuiddities(complementID qp.UUID, offset, limit uint64) (quiddityIDs []qp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// ListPriorities(quiddityID, complementID qp.UUID, offset, limit uint64) (priorities []uint64, nv storage_p.NumberOfVersion, err error_p.Error)

// ListMedias(quiddityID qp.UUID, offset, limit uint64) (objectIDs []op.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// ListRelates(objectID op.UUID, offset, limit uint64) (quiddityIDs []qp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// ListPriorities(objectID op.UUID, quiddityID qp.UUID, offset, limit uint64) (priorities []uint64, nv storage_p.NumberOfVersion, err error_p.Error)

// LIST_TaskIDs_BY_GroupID(groupID gp.UUID, offset, limit uint64) (taskIDs []tp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// LIST_GroupIDs_BY_TaskID(taskID tp.UUID, offset, limit uint64) (groupIDs []gp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

// 	LIST_ProjectIDs_By_GroupID_AND_Type(GroupID gp.UUID, t Type, offset, limit uint64) (projectIDs []pp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

// LIST_QuestionIDs_BY_RelationID(rID qp.UUID, offset, limit uint64) (questionIDs []qp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// LIST_QuestionIDs_BY_RelationID_AND_LabelID(rID qp.UUID, lID label_p.UUID, offset, limit uint64) (questionIDs []qp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
// LIST_RelationIDs_BY_QuestionIDs(qID qp.UUID, offset, limit uint64) (relationIDs []qp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

/*
type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(userID user_p.UUID, priority uint64) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(userID user_p.UUID, priority uint64, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	ListUser(groupID gp.UUID, offset, limit uint64) (userIDs []user_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	ListGroup(userID user_p.UUID, offset, limit uint64) (groupIDs []gp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	ListPriorities(userID user_p.UUID, groupID gp.UUID, offset, limit uint64) (priorities []uint64, nv storage_p.NumberOfVersion, err error_p.Error)

	// TODO:::
	// FilterByStatus(userID user_p.UUID, status Status, offset, limit uint64) (groupIDs []gp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
*/

/*
type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	// Count(questionID qp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	// Get(questionID qp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	// Count(labelID label_p.UUID, priority uint64) (nv storage_p.NumberOfVersion, err error_p.Error)
	// Get(labelID label_p.UUID, priority uint64, vo storage_p.VersionOffset) (f DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	// LIST_LabelIDs_BY_ItemID(itemID record_p.UUID, offset, limit uint64) (labelIDs []label_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	// LIST_Priorities_BY_LabelID(itemID record_p.UUID, labelID label_p.UUID, offset, limit uint64) (priorities []uint64, nv storage_p.NumberOfVersion, err error_p.Error)

	FIND_OtherIDs_BY_LabelID(labelID label_p.UUID, offset, limit uint64) (ids []record_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	LIST_LabelIDs_BY_OtherID(id record_p.UUID, offset, limit uint64) (labelIDs []label_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

	// FILTER_BY_Status(status Status, offset, limit uint64) (tags []string, nv storage_p.NumberOfVersion, err error_p.Error)
}
*/
