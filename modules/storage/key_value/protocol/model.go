/* For license and copyright information please see the LEGAL file in the code repository */

package kv_p

import (
	container_p "memar/computer/adt/container/protocol"
	error_p "memar/process/error/protocol"
)

// Model is the interface that show how an key-value directory work.
// If need encryption, Implement requirements at block storage level.
// https://github.com/cockroachdb/pebble/blob/master/open.go
type Model interface {
	KeyNumbers() (num container_p.NumberOfElement, err error_p.Error)
	ListKeys(offset container_p.ElementIndex, limit container_p.NumberOfElement) (keys []Key, err error_p.Error)

	Lock(key Key) (value Value, err error_p.Error)
	Unlock(key Key, value Value) (err error_p.Error)

	Length(key Key) (ln container_p.NumberOfElement, err error_p.Error)
	Get(key Key) (value Value, err error_p.Error)
	Set(key Key, value Value) (err error_p.Error)

	// make invisible just by remove from primary index
	Delete(key Key) (err error_p.Error)
	// make invisible by remove from primary index & write zero data to value location
	Erase(key Key) (err error_p.Error)

	// Multiple changes can be made in one atomic batch
	// Batch()
}
