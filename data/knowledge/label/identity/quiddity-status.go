/* For license and copyright information please see the LEGAL file in the code repository */

package label

/*
All quiddities even `label` itself CAN get `quiddity-status` labels.

Status indicate base record status
It is like labeling records But it is systematic labels.
Labels check in business rules logic(Async), but status check in services logic(Sync).
*/

// by owner
// Locked
// Expired

// by justice(admins) or fraud detection mechanism
// Blocked

// Due to some reason quiddity was Locked, Closed, ... and must not use or edit
//
// Failure
// PermanentInactivated
// TemporaryInactivated
// Hidden
// Deleted
// Revoked

// data is belong to other application(org) and add by users by GUI
// ManuallyAdded
//
// manual added data in some way was verified.
// ManuallyVerified
//
// Edited
