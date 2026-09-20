/* For license and copyright information please see the LEGAL file in the code repository */

package org

// // Transfer use
// func Transfer() {
// 	const productInventoryPath = "D:/SabzCity/platform/sabz.city/datastore-files/1086912575236019950"
// 	const hashPath = "D:/SabzCity/platform/sabz.city/datastore-files/14141993521672016749"
// 	const delPath = "D:/SabzCity/platform/sabz.city/datastore-files/del"
// 	const refDelPath = "D:/SabzCity/platform/sabz.city/datastore-files/refDel"

// 	var repoFiles []os.FileInfo
// 	var goErr error
// 	var err protocol.Error
// 	repoFiles, goErr = ioutil.ReadDir(productInventoryPath)
// 	if goErr != nil {
// 		return
// 	}
// 	file.SortFilesDec(repoFiles)

// 	var pi ProductInventory
// 	var hash [32]byte
// 	var hashName string
// 	for _, file := range repoFiles {
// 		var name = file.Metadata().URI().Name()
// 		log.Info("RecordName:", name)

// 		var data []byte
// 		data, goErr = ioutil.ReadFile(path.Join(productInventoryPath, name))
// 		if goErr != nil {
// 			log.Warn("ReadFile:", goErr)
// 			continue
// 		}

// 		err = pi.FromSyllab(data)
// 		if err != nil {
// 			log.Warn("FromSyllab", err)
// 			continue
// 		}

// 		hash = pi.hashQuiddityIDOwnerIDForRecordID()
// 		hashName = base64.RawURLEncoding.EncodeToString(hash[:])
// 		log.Info("hashQuiddityIDOwnerIDForRecordID:", hashName)
// 		goErr = os.Rename(path.Join(hashPath, hashName), path.Join(delPath, hashName))
// 		if goErr != nil {
// 			log.Warn("hashQuiddityIDOwnerIDForRecordID:", goErr)
// 		}
// 		pi.IndexRecordIDForQuiddityIDOwnerIDDaily()

// 		hash = pi.hashQuiddityIDDCIDForRecordID()
// 		hashName = base64.RawURLEncoding.EncodeToString(hash[:])
// 		log.Info("hashQuiddityIDDCIDForRecordID:", hashName)
// 		goErr = os.Rename(path.Join(hashPath, hashName), path.Join(delPath, hashName))
// 		if goErr != nil {
// 			log.Warn("hashQuiddityIDDCIDForRecordID:", goErr)
// 		}
// 		pi.IndexRecordIDForQuiddityIDDCIDDaily()

// 		hash = pi.hashOwnerIDForRecordIDDaily()
// 		hashName = base64.RawURLEncoding.EncodeToString(hash[:])
// 		log.Info("hashOwnerIDForRecordIDDaily:", hashName)
// 		goErr = os.Rename(path.Join(hashPath, hashName), path.Join(refDelPath, hashName))
// 		if goErr != nil {
// 			log.Warn("hashOwnerIDForRecordIDDaily:", goErr)
// 		}
// 		log.Info("-----------------------------------------------")
// 	}
// }

// /*
// 	-- PRIMARY INDEXES --
// */
// // IndexRecordIDForQuiddityIDOwnerID save RecordID chain for QuiddityID+OwnerID
// // Call in each update to the exiting record!
// func (pi *ProductInventory) IndexRecordIDForQuiddityIDOwnerID() {
// 	var indexRequest = pehrest.HashSetValueReq{
// 		Type:       ganjine.RequestTypeBroadcast,
// 		IndexKey:   pi.hashQuiddityIDOwnerIDForRecordID(),
// 		IndexValue: pi.RecordID,
// 	}
// 	var err = psdk.HashSetValue(&indexRequest)
// 	if err != nil {
// 		if protocol.AppDebugMode {
// 			log.Debug("Ganjine - IndexRecordIDForQuiddityIDOwnerID:", err)
// 		}
// 		// TODO::: we must retry more due to record wrote successfully!
// 	}
// }

// func (pi *ProductInventory) hashQuiddityIDOwnerIDForRecordID() (hash [32]byte) {
// 	const field = "QuiddityID+OwnerID"
// 	var buf = make([]byte, 72+len(field)) // 8+32+32
// 	syllab.SetUInt64(buf, 0, productInventoryStructureID)
// 	copy(buf[8:], pi.QuiddityID[:])
// 	copy(buf[40:], pi.OwnerID[:])
// 	copy(buf[72:], field)
// 	return sha512.Sum512_256(buf)
// }

// // IndexRecordIDForQuiddityIDDCID save RecordID chain for QuiddityID+DCID
// // Call in each update to the exiting record!
// func (pi *ProductInventory) IndexRecordIDForQuiddityIDDCID() {
// 	var indexRequest = pehrest.HashSetValueReq{
// 		Type:       ganjine.RequestTypeBroadcast,
// 		IndexKey:   pi.hashQuiddityIDDCIDForRecordID(),
// 		IndexValue: pi.RecordID,
// 	}
// 	var err = psdk.HashSetValue(&indexRequest)
// 	if err != nil {
// 		if protocol.AppDebugMode {
// 			log.Debug("Ganjine - IndexRecordIDForQuiddityIDDCID:", err)
// 		}
// 		// TODO::: we must retry more due to record wrote successfully!
// 	}
// }

// func (pi *ProductInventory) hashQuiddityIDDCIDForRecordID() (hash [32]byte) {
// 	const field = "QuiddityID+DCID"
// 	var buf = make([]byte, 72+len(field)) // 8+32+32
// 	syllab.SetUInt64(buf, 0, productInventoryStructureID)
// 	copy(buf[8:], pi.QuiddityID[:])
// 	copy(buf[40:], pi.DCID[:])
// 	copy(buf[72:], field)
// 	return sha512.Sum512_256(buf)
// }

// /*
// 	-- SECONDARY INDEXES --
// */

// func (pi *ProductInventory) hashOwnerIDForRecordIDDaily() (hash [32]byte) {
// 	const field = "ReferenceID"
// 	var buf = make([]byte, 40+len(field)) // 8+32
// 	syllab.SetUInt64(buf, 0, productInventoryStructureID)
// 	copy(buf[8:], pi.ReferenceID[:])
// 	copy(buf[40:], field)
// 	return sha512.Sum512_256(buf)
// }
