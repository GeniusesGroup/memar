## 
below text are `tree /F /A` output

```bash
C:.
|   .gitignore
|   app.service
|   Contribution.md
|   go.mod
|   go.work
|   go.work.sum
|   LEGAL
|   LICENSE
|   memar.config
|   README.md
|   repo_tree.md
|   staticcheck.conf
|
+---bin
+---bundles
|   +---Achaemenid
|   |   |   Achaemenid.md
|   |   |   init.go
|   |   |   README.md
|   |   |
|   |   \---achaemenid
|   |       |   application.go
|   |       |   application_test.go
|   |       |   cryptography.go
|   |       |   firewall.go
|   |       |   media-types.go
|   |       |   ____ai.go
|   |       |
|   |       \---errors
|   |               bad_request.go
|   |               bad_request.locale.eng.go
|   |               bad_response.go
|   |               bad_response.locale.eng.go
|   |               const.go
|   |               guest_connection_max_reached.go
|   |               guest_connection_max_reached.locale.eng.go
|   |               guest_connection_not_allow.go
|   |               guest_connection_not_allow.locale.eng.go
|   |               init.go
|   |               internal_error.go
|   |               internal_error.locale.eng.go
|   |               locale.eng.go
|   |               locale.per.go
|   |               not_standard_id.go
|   |               not_standard_id.locale.eng.go
|   |               protocol_handler.go
|   |               protocol_handler.locale.eng.go
|   |
|   +---bank
|   |       README.md
|   |
|   +---bot
|   +---call
|   |       README.md
|   |
|   +---chapar_khane
|   |   |   ChaparKhane.md
|   |   |   init-server.go
|   |   |   README.md
|   |   |
|   |   +---internal
|   |   |   \---router
|   |   |           connection-router.go
|   |   |           connection-user.go
|   |   |           connections-routers.go
|   |   |           connections-society.go
|   |   |           connections-users.go
|   |   |           manifest.go
|   |   |           security.go
|   |   |           server.go
|   |   |
|   |   \---services
|   |       |   service-release-gp-by-router.go
|   |       |   service-release-gp-by-user.go
|   |       |   service-router-advertisement.go
|   |       |   service-router-discovery.go
|   |       |   service-router-solicitation.go
|   |       |
|   |       +---chapar
|   |       |       connection-protocol.go
|   |       |       connections.go
|   |       |       topology.go
|   |       |
|   |       +---get-gp-by-router
|   |       |       logic.go
|   |       |
|   |       \---get-gp-by-user
|   |               logic.go
|   |               req.go
|   |               res.go
|   |               service.go
|   |
|   +---cli
|   |       init.go
|   |
|   +---cryptography
|   |       README.md
|   |
|   +---leadership
|   |       README.md
|   |
|   +---Dideban
|   |       README.md
|   |
|   +---Dokkan
|   |       README.md
|   |
|   +---economy
|   |       README.md
|   |
|   +---Ensan
|   |       README.md
|   |
|   +---Esteghrar
|   |       README.md
|   |
|   +---Ganjine
|   |       Ganjine.md
|   |       README.md
|   |
|   +---Gardanesh
|   |       README.md
|   |
|   +---government
|   |   |   README.md
|   |   |
|   |   \---protocol
|   |           dt-uuid.go
|   |
|   +---gui
|   |       init.go
|   |       main.go
|   |
|   +---Health
|   |       README.md
|   |       services.go
|   |
|   +---iaas
|   |       run-app
|   |       stop-app
|   |
|   +---information_system
|   |       README.md
|   |
|   +---insurance
|   |       README.md
|   |
|   +---justice
|   |       README.md
|   |
|   +---logistics
|   |       README.md
|   |
|   +---marketing
|   |       README.md
|   |
|   +---pay
|   |   \---protocol
|   |           data_model.go
|   |
|   +---Payam
|   |       README.md
|   |
|   +---Pehrest
|   |       README.md
|   |
|   +---planet
|   |   \---protocol
|   |           planet.go
|   |
|   +---supply-chain
|   |       README.md
|   |
|   \---value-chain
|           README.md
|
+---docs
|       code-rule-separation.md
|       connection-reuse.md
|       device-ownership-and-authority-transfer.md
|       task-concept.md
|       topic-case-dispute-domain.md
|       topic-code-rule-boundary-criteria.md
|       topic-coercion-graded-capability.md
|       topic-naming-organization-rationale.md
|       topic-organization-vs-group-boundary.md
|       topic-physical-security-requirement-modeling.md
|       user.md
|
+---modules
|   |   README.md
|   |   working on.go
|   |
|   +---ai
|   |   +---image
|   |   |   \---protocol
|   |   |           dt-type.go
|   |   |
|   |   +---text
|   |   |   \---protocol
|   |   |           dt-type.go
|   |   |
|   |   \---voice
|   |       \---protocol
|   |               dt-type.go
|   |
|   +---computer
|   |   |   application-engine.go
|   |   |   application.go
|   |   |   README.md
|   |   |
|   |   +---analytic
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---analysis
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---analytic
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---connection
|   |   |   |   label.go
|   |   |   |   README.md
|   |   |   |
|   |   |   +---analytics
|   |   |   |   +---conversion_rate
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---page-visited-utm
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-uuid.go
|   |   |   |   |           utm.go
|   |   |   |   |
|   |   |   |   +---user-activity
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---user-activity_rate
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-rate.go
|   |   |   |   |
|   |   |   |   +---user-activity_time
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---user-activity_time-utc_hour
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---user-average_activity-utc_day
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-average.go
|   |   |   |   |
|   |   |   |   +---user-online_count-utc_hour
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-online_count.go
|   |   |   |   |
|   |   |   |   +---users-bounce_rate
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---users-count-utc_hour
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---users-gender_count
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---users-gender_count-utc_hour
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-average.go
|   |   |   |   |
|   |   |   |   +---users-gender_count-utc_minute
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---users-onlive_counts-utc_hour
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-online_count.go
|   |   |   |   |
|   |   |   |   +---users-sexuality_count
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-count.go
|   |   |   |   |
|   |   |   |   +---users-sexuality_count-utc_hour
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-count.go
|   |   |   |   |
|   |   |   |   \---utm
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---authenticated_by
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---services
|   |   |   |   |       \---authenticate-app-connection
|   |   |   |   |               logic.go
|   |   |   |   |
|   |   |   |   +---authorize_by
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---connection_to
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---metrics
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   +---internal
|   |   |   |   |   |       connection-metric.go
|   |   |   |   |   |       connection-metric_test.go
|   |   |   |   |   |       connections-metric.go
|   |   |   |   |   |       connections-metric_test.go
|   |   |   |   |   |       networking-metric.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           bs_.go
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---net-gp
|   |   |   |   |       connections.go
|   |   |   |   |       connections_test.go
|   |   |   |   |
|   |   |   |   +---page-visited
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   +---protocol
|   |   |   |   |   |       data_model.go
|   |   |   |   |   |
|   |   |   |   |   \---services
|   |   |   |   \---request
|   |   |   |           label.go
|   |   |   |
|   |   |   +---edges-loop
|   |   |   +---protocol
|   |   |   |       data_model.go
|   |   |   |       dt-cipher_suite.go
|   |   |   |       dt-uuid.go
|   |   |   |       protocol.go
|   |   |   |
|   |   |   +---services
|   |   |   |       service-close-connection.go
|   |   |   |       service-get-streams-ids.go
|   |   |   |       service-revoke-connection.go
|   |   |   |       service-set-connection-settings.go
|   |   |   |       service-set-connection-thing-id.go
|   |   |   |       service-transfer-app-connection.go
|   |   |   |
|   |   |   +---status
|   |   |   |       connection-status.go
|   |   |   |
|   |   |   \---_____old
|   |   |           connections.go
|   |   |           errors.go
|   |   |           service-edit-person-connection.go
|   |   |           service-find-user-app-connection-by-given-delegate.go
|   |   |           service-find-user-app-connection-by-gotten-delegate.go
|   |   |           service-find-user-app-connection.go
|   |   |           service-get-connection.go
|   |   |           service-get-connections-id.go
|   |   |           service-get-user-app-connection.go
|   |   |           service-register-user-app-connection.go
|   |   |           service-revoke-user-app-connection.go
|   |   |           service-set-connection-usage.go
|   |   |           service-update-user-app-connection.go
|   |   |           storage.go
|   |   |           user-app-connection-metric.go
|   |   |
|   |   +---datatype
|   |   |   |   label.go
|   |   |   |
|   |   |   +---edges
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---device
|   |   |   |   README.md
|   |   |   |
|   |   |   +---data
|   |   |   |   +---sensor-co2
|   |   |   |   +---sensor-o2
|   |   |   |   +---sensor-pressure
|   |   |   |   +---sensor-temperature
|   |   |   |   |   \---services
|   |   |   |   |       \---save
|   |   |   |   |               logic.go
|   |   |   |   |
|   |   |   |   +---thing-camera
|   |   |   |   +---thing-door
|   |   |   |   +---thing-hvac
|   |   |   |   +---thing-lamp
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-switch_type.go
|   |   |   |   |
|   |   |   |   +---thing-monitor
|   |   |   |   +---thing-oven
|   |   |   |   \---thing-sound
|   |   |   +---edges
|   |   |   |   |   thing-channel-status.go
|   |   |   |   |   thing-relation-org.go
|   |   |   |   |
|   |   |   |   +---channel_of
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---driver
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---signal-input
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---signal-output
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-signal_data.go
|   |   |           dt-uuid.go
|   |   |           service-signal-find.go
|   |   |           service-signal-get.go
|   |   |           service-signal-save.go
|   |   |
|   |   +---error
|   |   |   |   label.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---services
|   |   |           get-platform-error-detail.go
|   |   |           get-platform-errors-js-sdk.go
|   |   |
|   |   +---event
|   |   +---hardware
|   |   |   +---edges
|   |   |   |   |   hardware-status.go
|   |   |   |   |
|   |   |   |   \---hardware
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |           dt-uuid.go
|   |   |           storage.go
|   |   |
|   |   +---instance_of
|   |   |   |   init.go
|   |   |   |   label.go
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   net-address.go
|   |   |   |   |   node-relation-hardware.go
|   |   |   |   |   node-relation-node.go
|   |   |   |   |   node-resource.go
|   |   |   |   |   node-status.go
|   |   |   |   |   node.go
|   |   |   |   |
|   |   |   |   +---address
|   |   |   |   |   \---protocol
|   |   |   |   |           bs.go
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-address.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---audit-log
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   +---protocol
|   |   |   |   |   |       config.go
|   |   |   |   |   |       data_model.go
|   |   |   |   |   |
|   |   |   |   |   \---services
|   |   |   |   |       \---listener
|   |   |   |   |           |   logic.go
|   |   |   |   |           |
|   |   |   |   |           \---internal
|   |   |   |   |                   event.go
|   |   |   |   |                   log.go
|   |   |   |   |
|   |   |   |   +---health
|   |   |   |   |   +---protocol
|   |   |   |   |   |       business-services.go
|   |   |   |   |   |       data_model.go
|   |   |   |   |   |
|   |   |   |   |   \---services
|   |   |   |   |       \---ping
|   |   |   |   |               frame-ping.go
|   |   |   |   |
|   |   |   |   +---language-human
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---node
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           distributed-cluster.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---node-metric
|   |   |   |   |       make-main-file.go
|   |   |   |   |       manifest.go
|   |   |   |   |
|   |   |   |   +---resource
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-resource_type.go
|   |   |   |   |
|   |   |   |   \---user-active
|   |   |   |           label.go
|   |   |   |           users.go
|   |   |   |
|   |   |   +---errors
|   |   |   |       errors.go
|   |   |   |       locale.eng.go
|   |   |   |       locale.per.go
|   |   |   |
|   |   |   +---internal
|   |   |   |   \---node
|   |   |   |           data-structure-node.go
|   |   |   |           node.go
|   |   |   |           nodes.go
|   |   |   |           replication.go
|   |   |   |           replications.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---services
|   |   |           service-get-node-details.go
|   |   |           service-get-server-nodes-sdk.go
|   |   |           service-get-server-nodes.go
|   |   |           service-ping-peer.go
|   |   |           service-sync-time.go
|   |   |
|   |   +---module
|   |   |   |   label.go
|   |   |   |   README.md
|   |   |   |
|   |   |   \---protocol
|   |   |           bs.go
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---notification
|   |   |   +---edges
|   |   |   |   |   notification.go
|   |   |   |   |
|   |   |   |   +---last_dispatch
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---listener
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---listener-ack
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---signal_preference
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-signal_preference.go
|   |   |   |   |
|   |   |   |   +---when-utc
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   \---why
|   |   |   |           label.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---rules
|   |   |       \---log-listener
|   |   |           |   label.go
|   |   |           |
|   |   |           \---protocol
|   |   |                   data_model.go
|   |   |                   ss-event_target.go
|   |   |
|   |   +---page
|   |   |   +---analytics
|   |   |   +---edges
|   |   |   |   |   label.go
|   |   |   |   |   page.go
|   |   |   |   |
|   |   |   |   +---code
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   \---manifest
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---request
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---authorized
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-authorized-by.go
|   |   |   |   |
|   |   |   |   +---connection
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---data
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-request-data.go
|   |   |   |   |
|   |   |   |   +---last-chain
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---service
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---signature
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-signature.go
|   |   |   |   |
|   |   |   |   +---sub-request
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---time
|   |   |   |           label.go
|   |   |   |
|   |   |   +---edges-loop
|   |   |   |   +---logic-base
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---logic-rollback
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---logic-side
|   |   |   |           label.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |       storage.go
|   |   |   |
|   |   |   \---widget
|   |   |       \---protocol
|   |   |               data_model.go
|   |   |               storage.go
|   |   |
|   |   +---rule
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---authorization
|   |   |   |   |   |   init.go
|   |   |   |   |   |   README.md
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-authorized-by.go
|   |   |   |   |
|   |   |   |   +---checked
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---code
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---execution-limit_to_label
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---execution-limit_to_node
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---initiator-event
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---initiator-service
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---request
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---task_reason
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---time_limit
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   \---uml
|   |   |   |           init.go
|   |   |   |           README.md
|   |   |   |
|   |   |   +---edges-loop
|   |   |   |   +---access_control
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---checker
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---manual_call
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---repeatable
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---rule
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   \---synchronous
|   |   |   |           init.go
|   |   |   |           README.md
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |       model.go
|   |   |   |       storage.go
|   |   |   |
|   |   |   +---rules
|   |   |   \---status
|   |   |           rule-status.go
|   |   |
|   |   +---service
|   |   |   +---edges
|   |   |   |       label.go
|   |   |   |       service-relation-module.go
|   |   |   |       service-relation-service.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---software
|   |   |   +---edges
|   |   |   |   |   app-relation-app.go
|   |   |   |   |   app-relation-module.go
|   |   |   |   |   app-relation-object.go
|   |   |   |   |   app-relation-page.go
|   |   |   |   |   app-relation-widget.go
|   |   |   |   |   app.go
|   |   |   |   |   rule-relation-app.go
|   |   |   |   |
|   |   |   |   +---accepted_protocols
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-ap.go
|   |   |   |   |
|   |   |   |   +---authentication-deny_password
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---authentication-force_use_2factor
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---configuration
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---language-human
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---language-human-ability
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---manifest
|   |   |   |       +---protocol
|   |   |   |       |       data_model.go
|   |   |   |       |
|   |   |   |       \---services
|   |   |   |               manifest.go
|   |   |   |               manifest_test.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---source-control
|   |   |   \---rule-statement
|   |   |       \---protocol
|   |   |               data_model.go
|   |   |               dt-rule-step-id.go
|   |   |
|   |   +---token
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---code_security
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---expire_date
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---key_private
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---key_public
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   +---protocol
|   |   |   |   |   |       data_model.go
|   |   |   |   |   |       dt-public_key.go
|   |   |   |   |   |       dt-uuid.go
|   |   |   |   |   |
|   |   |   |   |   \---services
|   |   |   |   |       \---user-public-key
|   |   |   |   |               approve-person-public-key.go
|   |   |   |   |               authenticate-person-public-key.go
|   |   |   |   |               revoke-person-public-key.go
|   |   |   |   |               storage.go
|   |   |   |   |
|   |   |   |   +---key_symmetric
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---oauth2
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---otp
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-otp_key.go
|   |   |   |   |
|   |   |   |   +---otp-addition
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   +---errors
|   |   |   |   |   |       errors.go
|   |   |   |   |   |       locale.eng.go
|   |   |   |   |   |       locale.per.go
|   |   |   |   |   |
|   |   |   |   |   +---internal
|   |   |   |   |   |   \---generator
|   |   |   |   |   |           totp.go
|   |   |   |   |   |           totp_test.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---password
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           business-services.go
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-password_hash.go
|   |   |   |   |
|   |   |   |   +---pin
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---revoked
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---token
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---widget
|   |   |   |   label.go
|   |   |   |
|   |   |   +---edges
|   |   |   |       widget.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   \---www
|   |       +---internal
|   |       |   |   assets.go
|   |       |   |   combine.go
|   |       |   |   css.go
|   |       |   |   html.go
|   |       |   |   js.go
|   |       |   |   media-types.go
|   |       |   |
|   |       |   +---browser
|   |       |   |       browser.go
|   |       |   |
|   |       |   +---css
|   |       |   +---errors
|   |       |   |       errors.go
|   |       |   |
|   |       |   +---html
|   |       |   |       render.go
|   |       |   |
|   |       |   \---js
|   |       +---protocol
|   |       \---services
|   |           +---host-supported
|   |           |       host-supported.go
|   |           |
|   |           +---landings
|   |           |       landing.go
|   |           |
|   |           +---middleware-old-browser
|   |           |       logic.go
|   |           |
|   |           +---mux
|   |           |       locale.eng.go
|   |           |       mux.go
|   |           |       service.go
|   |           |       services.go
|   |           |
|   |           +---not_exist
|   |           |       not_exist.go
|   |           |
|   |           +---serve-files
|   |           |       locale.eng.go
|   |           |       serve-www.go
|   |           |
|   |           \---twitter-card
|   |                   logic.go
|   |
|   +---economics
|   |   |   README.md
|   |   |
|   |   +---account
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---bookkeeping
|   |   |   |   |   |   label.go
|   |   |   |   |   |   README.md
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           business-services.go
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-transaction-index.go
|   |   |   |   |           ss-event_target.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   \---settlement
|   |   |   |       |   label.go
|   |   |   |       |   README.md
|   |   |   |       |
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               storage.go
|   |   |   |
|   |   |   +---edges-loop
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---invoice
|   |   |   |   README.md
|   |   |   |
|   |   |   +---analytics
|   |   |   |   +---discount_usage-utc-day
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---discount_usage-utc-minute
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   \---disount_rate
|   |   |   +---edges
|   |   |   |   +---item
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-uuid.go
|   |   |   |   |           gui-widget.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---Item-ingredient
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           business-services.go
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-status.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---item-seat
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           business-services.go
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-seat_id.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---pay_by
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---pos-editor
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---pos-issuer
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---rule-enforcement
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---status
|   |   |   |   |       expired.go
|   |   |   |   |       invoice-status.go
|   |   |   |   |       paid-partially.go
|   |   |   |   |       paid.go
|   |   |   |   |       voided.go
|   |   |   |   |
|   |   |   |   +---summary
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           ss-event_target.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---user-agent
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-applicant
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-broker
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-buyer
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-consumer
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-customer
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-franchise
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-orderer
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-payer
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-provider
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---user-seller
|   |   |   |           label.go
|   |   |   |
|   |   |   +---edges-shortcut
|   |   |   |   \---pre-order
|   |   |   |           init.go
|   |   |   |           README.md
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---rules
|   |   |       +---club-coin
|   |   |       |       label.go
|   |   |       |
|   |   |       +---discount
|   |   |       |   |   label.go
|   |   |       |   |
|   |   |       |   \---protocol
|   |   |       |           area.go
|   |   |       |           group.go
|   |   |       |           invoice.go
|   |   |       |           label.go
|   |   |       |           location.go
|   |   |       |           pos.go
|   |   |       |           product.go
|   |   |       |           time-validity.go
|   |   |       |           timing-utc.go
|   |   |       |           usage.go
|   |   |       |           user-type.go
|   |   |       |           user.go
|   |   |       |           value.go
|   |   |       |
|   |   |       +---discount-packages
|   |   |       |   |   logic.go
|   |   |       |   |
|   |   |       |   +---bundle
|   |   |       |   \---protocol
|   |   |       |           business-services.go
|   |   |       |
|   |   |       +---gift-product
|   |   |       |       label.go
|   |   |       |
|   |   |       +---refund
|   |   |       |       label.go
|   |   |       |
|   |   |       \---voucher
|   |   |           |   label.go
|   |   |           |
|   |   |           +---analytics
|   |   |           |   +---voucher_issued-utc_hour
|   |   |           |   |   \---protocol
|   |   |           |   |           data_model.go
|   |   |           |   |           storage.go
|   |   |           |   |
|   |   |           |   \---voucher_issued-utc_minute
|   |   |           |       \---protocol
|   |   |           |               data_model.go
|   |   |           |               storage.go
|   |   |           |
|   |   |           \---protocol
|   |   |                   dt-each.go
|   |   |                   dt-invoice-type.go
|   |   |                   dt-max_each_use.go
|   |   |                   dt-proportion.go
|   |   |                   dt-worth.go
|   |   |                   duration.go
|   |   |                   estate.go
|   |   |                   group.go
|   |   |                   invoice.go
|   |   |                   label.go
|   |   |                   pos.go
|   |   |                   product.go
|   |   |                   user.go
|   |   |                   value.go
|   |   |
|   |   +---product
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   product-relation-content.go
|   |   |   |   |   product-relation-group.go
|   |   |   |   |   product-relation-label.go
|   |   |   |   |   product-relation-product.go
|   |   |   |   |   product-relation-rule.go
|   |   |   |   |   product-relation-staff.go
|   |   |   |   |   product-relation-user.go
|   |   |   |   |   product.go
|   |   |   |   |
|   |   |   |   +---brand
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---buy-limit
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---customable
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---price
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---price-payable
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---price-settlement
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---pricing
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---status
|   |   |   |           product-status.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   \---transaction
|   |       |   README.md
|   |       |
|   |       +---edges
|   |       |   +---account-from
|   |       |   |   |   init.go
|   |       |   |   |   README.md
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           data_model.go
|   |       |   |
|   |       |   +---account-to
|   |       |   |       init.go
|   |       |   |       README.md
|   |       |   |
|   |       |   +---conditional
|   |       |   |       init.go
|   |       |   |       README.md
|   |       |   |
|   |       |   \---reference
|   |       |       |   label.go
|   |       |       |   README.md
|   |       |       |
|   |       |       \---protocol
|   |       |               data_model.go
|   |       |
|   |       +---edges-loop
|   |       +---edges-shortcut
|   |       |       transaction.go
|   |       |
|   |       +---protocol
|   |       |       data_model.go
|   |       |       dt-uuid.go
|   |       |       model.go
|   |       |       storage.go
|   |       |
|   |       +---services
|   |       \---status
|   |               transaction-status.go
|   |
|   +---gui
|   |   +---page-automating-processes
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |
|   |   +---page-comments
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |           errors.go
|   |   |
|   |   +---page-content
|   |   |   |   content.css
|   |   |   |   content.html
|   |   |   |   content.js
|   |   |   |
|   |   |   \---protocol
|   |   |           business-services.go
|   |   |           data_model.go
|   |   |           storage.go
|   |   |
|   |   +---page-contents
|   |   |       contents.css
|   |   |       contents.html
|   |   |       contents.js
|   |   |
|   |   +---page-contract
|   |   |       contract.css
|   |   |       contract.html
|   |   |       contract.js
|   |   |
|   |   +---page-discussion
|   |   |   \---protocol
|   |   |           gui-page.go
|   |   |
|   |   +---page-economic-indicator
|   |   |       README.md
|   |   |
|   |   +---page-financial-accounts
|   |   |       accounts.css
|   |   |       accounts.html
|   |   |       accounts.js
|   |   |
|   |   +---page-friendship_cycle
|   |   |   \---protocol
|   |   |           gui-page.go
|   |   |
|   |   +---page-inventory
|   |   |   |   distribute-status.go
|   |   |   |   README.md
|   |   |   |
|   |   |   +---protocol
|   |   |   |       data_model.go
|   |   |   |       dt-reference_type.go
|   |   |   |       dt-uuid.go
|   |   |   |       gui-widget.go
|   |   |   |       storage.go
|   |   |   |
|   |   |   \---widget-distribute
|   |   |       \---protocol
|   |   |               data_model.go
|   |   |               storage.go
|   |   |
|   |   +---page-invoice
|   |   |   \---protocol
|   |   |           gui-page.go
|   |   |           gui-widget.go
|   |   |
|   |   +---page-invoices
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |
|   |   +---page-labels
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |
|   |   +---page-logIn
|   |   |       logIn.css
|   |   |       logIn.html
|   |   |       logIn.js
|   |   |
|   |   +---page-market
|   |   |   |   README.md
|   |   |   |
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |
|   |   +---page-market-booth
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |
|   |   +---page-marketing-analytic
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |
|   |   +---page-org-staff
|   |   |       staff.css
|   |   |       staff.html
|   |   |       staff.js
|   |   |
|   |   +---page-process
|   |   |       README.md
|   |   |
|   |   +---page-product
|   |   |   \---protocol
|   |   |           gui-page.go
|   |   |
|   |   +---page-products
|   |   |   \---protocol
|   |   |           gui-page.go
|   |   |
|   |   +---page-questionnarie
|   |   |   \---protocol
|   |   |           gui-page.go
|   |   |
|   |   +---page-quiddity
|   |   |       widget-user-relation-user.go
|   |   |
|   |   +---page-scm
|   |   +---page-service
|   |   |   +---errors
|   |   |   |       errors.go
|   |   |   |
|   |   |   +---protocol
|   |   |   \---services
|   |   |       \---get_detail
|   |   |               request.go
|   |   |               response.go
|   |   |               server.go
|   |   |               service.go
|   |   |
|   |   +---page-services
|   |   |   \---protocol
|   |   |           bs-get_detail.go
|   |   |
|   |   +---page-staffs
|   |   |       storage.go
|   |   |
|   |   +---page-tasks
|   |   |       storage.go
|   |   |
|   |   +---page-user
|   |   |   \---protocol
|   |   |           gui-page.go
|   |   |           widget-user-relation-org.go
|   |   |
|   |   \---page-work_flow
|   |           README.md
|   |
|   +---identity
|   |   |   README.md
|   |   |
|   |   +---bot
|   |   |   |   README.md
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---business
|   |   |       README.md
|   |   |
|   |   +---estate
|   |   |   |   README.md
|   |   |   |
|   |   |   +---analytics
|   |   |   |   +---geography-coordinate
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   \---geography-coordinate-analytic
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---neighbors_conflict
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---relation-born_in
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---relation-live_in
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---relation-neighborhood
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---relation-part
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---relation-work_in
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-alley
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-apartment
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-block
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-boulevard
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-building
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-city
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-commercial
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-continent
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-country
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-district
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-hall
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-house
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-land
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-lobby
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-parking
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-planet
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-province
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-region
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-residential
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-space
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-state
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-storage
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---type-street
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---type-warehouse
|   |   |   |   |   |   label.go
|   |   |   |   |   |   README.md
|   |   |   |   |   |
|   |   |   |   |   +---edges
|   |   |   |   |   |       estate-relation-product.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-uuid.go
|   |   |   |   |
|   |   |   |   +---type-way
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   \---type-zone
|   |   |   |           label.go
|   |   |   |           README.md
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---government
|   |   |   +---edges
|   |   |   \---rules
|   |   |           rule.go
|   |   |
|   |   +---object
|   |   |   +---edges
|   |   |   |   +---coordinate-boundary-gps
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---coordinate-gps
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-uuid.go
|   |   |   |   |
|   |   |   |   +---model-physical
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---model-plane-horizontal
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---model-structure
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---model-volume
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---movable
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---objective
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---organization
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   organization-relation-organization.go
|   |   |   |   |   organization.go
|   |   |   |   |   user-relation-org.go
|   |   |   |   |
|   |   |   |   \---organization
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---person
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---person
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---social_connections
|   |   |   |       |   README.md
|   |   |   |       |   user-relation-user.go
|   |   |   |       |
|   |   |   |       +---brother
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---co-worker
|   |   |   |       +---connection
|   |   |   |       |   |   label.go
|   |   |   |       |   |
|   |   |   |       |   \---protocol
|   |   |   |       |           data_model.go
|   |   |   |       |
|   |   |   |       +---connection-1st
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---connection-2nd
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---connection-3rd
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---father
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---friendship
|   |   |   |       |   |   label.go
|   |   |   |       |   |
|   |   |   |       |   \---protocol
|   |   |   |       |           data_model.go
|   |   |   |       |
|   |   |   |       +---friendship-1st
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---friendship-2nd
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---known
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---mentee
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---mentor
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---mother
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       +---sister
|   |   |   |       |       label.go
|   |   |   |       |
|   |   |   |       \---works-with
|   |   |   |               label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---society
|   |   |   +---edges
|   |   |   |   +---relation-national_of
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---social_score
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           society.go
|   |   |
|   |   +---subject
|   |   |   +---edges
|   |   |   |   \---subject
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---taxon
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---animal
|   |   |   |   +---eukaryote
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---gender
|   |   |   |   |   |   init.go
|   |   |   |   |   |   README.md
|   |   |   |   |   |   validator.go
|   |   |   |   |   |
|   |   |   |   |   +---data
|   |   |   |   |   |       user-gender.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-uuid.go
|   |   |   |   |           model.go
|   |   |   |   |
|   |   |   |   +---organism
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---plant
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---sexuality
|   |   |   |   |   |   init.go
|   |   |   |   |   |   README.md
|   |   |   |   |   |
|   |   |   |   |   +---data
|   |   |   |   |   |       user-sexuality.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-uuid.go
|   |   |   |   |           model.go
|   |   |   |   |
|   |   |   |   +---taxonomic-rank
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---taxonomic-rank-class
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---taxonomic-rank-domain
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---taxonomic-rank-family
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---taxonomic-rank-genus
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---taxonomic-rank-kingdom
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---taxonomic-rank-life
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---taxonomic-rank-order
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---taxonomic-rank-phylum
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---taxonomic-rank-species
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---virus
|   |   |   |           README.md
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---thing
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   user-relation-object.go
|   |   |   |   |
|   |   |   |   +---complement
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---count_unit
|   |   |   |   |   |   label.go
|   |   |   |   |   |   README.md
|   |   |   |   |   |
|   |   |   |   |   +---labels
|   |   |   |   |   |   +---currencies
|   |   |   |   |   |   |   +---dollar-us
|   |   |   |   |   |   |   \---rial-iran
|   |   |   |   |   |   \---currency
|   |   |   |   |   |       |   label.go
|   |   |   |   |   |       |
|   |   |   |   |   |       +---edges
|   |   |   |   |   |       |       currency.go
|   |   |   |   |   |       |
|   |   |   |   |   |       \---protocol
|   |   |   |   |   |               dt-uuid.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-uuid.go
|   |   |   |   |
|   |   |   |   +---criterion
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-point.go
|   |   |   |   |           dt-type.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---datatype
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---icon
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---picture
|   |   |   |   |       obejct.go
|   |   |   |   |
|   |   |   |   +---substitute
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---template
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-uuid.go
|   |   |   |   |
|   |   |   |   \---thing
|   |   |   |           label.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |       model.go
|   |   |   |
|   |   |   \---widgets
|   |   |       \---ai_generated
|   |   |               logic
|   |   |
|   |   +---time
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---epoch
|   |   |   |   \---ttl
|   |   |   |       |   label.go
|   |   |   |       |
|   |   |   |       \---protocol
|   |   |   |               ttl.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---uri
|   |   |   +---edges
|   |   |   |   +---preview_link
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---uri
|   |   |   |           label.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |       model.go
|   |   |   |
|   |   |   \---widgets
|   |   |       \---quiddity-uri
|   |   |           \---protocol
|   |   |                   data_model.go
|   |   |                   dt-uri.go
|   |   |                   storage.go
|   |   |
|   |   \---user
|   |       |   README.md
|   |       |
|   |       +---edges
|   |       +---internal
|   |       |   |   user-type.go
|   |       |   |   user-type_test.go
|   |       |   |   user.go
|   |       |   |
|   |       |   \---identity
|   |       \---protocol
|   |               dt-id.go
|   |               dt-type.go
|   |               dt-uuid.go
|   |               model.go
|   |
|   +---knowledge
|   |   |   README.md
|   |   |
|   |   +---answer
|   |   |   +---edges
|   |   |   |   |   answer-result.go
|   |   |   |   |
|   |   |   |   +---descriptive
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---fill_in_the_blank
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---matching
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---object
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---option-multiple
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---option-ordering
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---option-single
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   \---rating
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               dt-answer.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---widgets
|   |   |       \---answer
|   |   +---certificate
|   |   |   +---edges
|   |   |   |   \---issuer
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |           dt-uuid.go
|   |   |
|   |   +---content
|   |   |   +---edges
|   |   |   |   |   content-relation-content.go
|   |   |   |   |
|   |   |   |   +---attach
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---delivered
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---email
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---forward
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---forward-limit_to_label
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---forward-limit_to_user
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---preview_link
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---quote
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---quote-limit_to_label
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---quote-limit_to_user
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---read
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---reply
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---reply-limit_per_user
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---reply-limit_to_label
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---reply-limit_to_user
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---seen
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---status
|   |   |   |           content-status.go
|   |   |   |
|   |   |   +---edges-loop
|   |   |   |   +---album
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---article
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---blog_post
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---book
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---comment
|   |   |   |   |   |   label.go
|   |   |   |   |   |   README.md
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-uuid.go
|   |   |   |   |
|   |   |   |   +---concert
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---confidential
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---course
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---game
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---movie
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---music
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---music_video
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---news
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---newsletter
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---podcast
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---serial
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---serial-episode
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---sport_game
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---tutorial
|   |   |   |           label.go
|   |   |   |
|   |   |   +---edges-shortcut
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---widgets
|   |   |       +---errors
|   |   |       +---forward
|   |   |       |       forward-limit_to_me.go
|   |   |       |
|   |   |       +---group
|   |   |       |   \---protocol
|   |   |       |           business-services.go
|   |   |       |           data_model.go
|   |   |       |           dt-comment-index.go
|   |   |       |           gui-widget.go
|   |   |       |           ss-event_target.go
|   |   |       |           storage.go
|   |   |       |
|   |   |       +---group-user
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |           ss-event_target.go
|   |   |       |           storage.go
|   |   |       |
|   |   |       +---log-activity
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |           storage.go
|   |   |       |
|   |   |       +---mentioned
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |           ss-event_target.go
|   |   |       |           storage.go
|   |   |       |
|   |   |       +---object
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |           storage.go
|   |   |       |
|   |   |       +---pin
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |           gui-widget.go
|   |   |       |           storage.go
|   |   |       |
|   |   |       +---protocol
|   |   |       |       dt-type.go
|   |   |       |       widget.go
|   |   |       |
|   |   |       +---quote
|   |   |       |       quote-limit_to_me.go
|   |   |       |
|   |   |       +---reply
|   |   |       |   |   reply-limit_to_me.go
|   |   |       |   |
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |           gui-widget.go
|   |   |       |           storage.go
|   |   |       |
|   |   |       +---tag
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |           storage.go
|   |   |       |
|   |   |       +---thread
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |
|   |   |       \---user_status
|   |   |           \---protocol
|   |   |                   data_model.go
|   |   |                   dt-status.go
|   |   |                   gui-widget.go
|   |   |                   storage.go
|   |   |
|   |   +---edge
|   |   |   +---edges
|   |   |   |   +---edge
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---loop_edge
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---preference
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---form
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   form-relation-form.go
|   |   |   |   |   form-relation-group.go
|   |   |   |   |   form-relation-knowledge_unit.go
|   |   |   |   |   form-relation-question.go
|   |   |   |   |   form-relation-task.go
|   |   |   |   |   form-respondent-relation-task.go
|   |   |   |   |   form-status.go
|   |   |   |   |   form.go
|   |   |   |   |
|   |   |   |   \---max-attempt
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               storage.go
|   |   |   |
|   |   |   +---edges-loop
|   |   |   |   +---exam
|   |   |   |   +---poll
|   |   |   |   \---questionnaire
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---form-respondent
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |           dt-uuid.go
|   |   |           storage.go
|   |   |
|   |   +---knowledge_unit
|   |   |   |   README.md
|   |   |   |
|   |   |   +---analytics
|   |   |   |   \---edu-score
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   knowledge_unit-relation-content.go
|   |   |   |   |   knowledge_unit-relation-knowledge_unit.go
|   |   |   |   |   knowledge_unit-relation-user.go
|   |   |   |   |   knowledge_unit.go
|   |   |   |   |
|   |   |   |   +---duration
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---endorse
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   \---score
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---label
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---label
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---label-allowed
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           config.go
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---label-used_by
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---list
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   +---protocol
|   |   |   |   |   |       business-services.go
|   |   |   |   |   |       data_model.go
|   |   |   |   |   |
|   |   |   |   |   \---services
|   |   |   |   |       \---set
|   |   |   |   |               init.go
|   |   |   |   |
|   |   |   |   +---matrix
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---table
|   |   |   |       |   label.go
|   |   |   |       |
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               dt-uuid.go
|   |   |   |               model.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |       model.go
|   |   |   |
|   |   |   \---widgets
|   |   |       \---categories
|   |   |           \---protocol
|   |   |                   data_model.go
|   |   |                   storage.go
|   |   |
|   |   +---language-human
|   |   |   |   label.go
|   |   |   |
|   |   |   +---errors
|   |   |   |       errors.go
|   |   |   |       locale.eng.go
|   |   |   |       locale.per.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---question
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   question-rating.go
|   |   |   |   |   question-relation-question.go
|   |   |   |   |   question-status.go
|   |   |   |   |   question.go
|   |   |   |   |
|   |   |   |   +---description
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---descriptive
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-type.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---limit
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---matching
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---max_attempt
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---multiple_choice
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---object
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---options
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-algorithm_type.go
|   |   |   |   |           dt-type.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---options-ordering
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---rating
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-type.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---rating-colors
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---rating-emoji
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---rating-labels
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   \---rating-relation
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               dt-type.go
|   |   |   |               storage.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---widgets
|   |   |       \---question
|   |   |               gui.go
|   |   |               storage.go
|   |   |
|   |   +---question_option
|   |   |   +---edges
|   |   |   |   |   question_option-relation-form.go
|   |   |   |   |   question_option-relation-question.go
|   |   |   |   |   question_option-relation-question_option.go
|   |   |   |   |
|   |   |   |   +---analytical
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   \---target
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               storage.go
|   |   |   |
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |           dt-type.go
|   |   |           dt-uuid.go
|   |   |           storage.go
|   |   |
|   |   +---reaction
|   |   |   |   README.md
|   |   |   |
|   |   |   \---edges
|   |   |       +---reaction
|   |   |       |   |   label.go
|   |   |       |   |
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |
|   |   |       +---reaction-count
|   |   |       |       label.go
|   |   |       |
|   |   |       \---reactionable
|   |   |               label.go
|   |   |
|   |   +---skill
|   |   |   |   label.go
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   skill.go
|   |   |   |   |
|   |   |   |   \---endorse
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |           dt-uuid.go
|   |   |
|   |   +---status
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   estate-status.go
|   |   |   |   |   quiddity-status.go
|   |   |   |   |   request-status.go
|   |   |   |   |
|   |   |   |   +---approval_needed
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---approved
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---block
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---deleted
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---draft
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---edited
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---failed
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---hidden
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---incompatibility
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---lock
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---optional
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---read-only
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---request
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---suggest
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-status.go
|   |   |           dt-uuid.go
|   |   |
|   |   \---text
|   |       |   README.md
|   |       |
|   |       +---analytics
|   |       |   \---search-analytic
|   |       |       \---protocol
|   |       |               data_model.go
|   |       |
|   |       +---edges
|   |       |   +---citations_number
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           bs-citation_numbers.go
|   |       |   |
|   |       |   +---duration
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           data_model.go
|   |       |   |           storage.go
|   |       |   |
|   |       |   +---hashtag
|   |       |   |       label.go
|   |       |   |
|   |       |   +---language
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   +---labels
|   |       |   |   |   |   dt-language.go
|   |       |   |   |   |
|   |       |   |   |   +---english
|   |       |   |   |   +---internal
|   |       |   |   |   |       languages.go
|   |       |   |   |   |       unsafe.go
|   |       |   |   |   |
|   |       |   |   |   \---persian
|   |       |   |   \---protocol
|   |       |   |           data_model.go
|   |       |   |
|   |       |   +---match-exactly
|   |       |   |       init.go
|   |       |   |       README.md
|   |       |   |
|   |       |   +---match-indirectly
|   |       |   |       label.go
|   |       |   |
|   |       |   +---match-partly
|   |       |   |       label.go
|   |       |   |
|   |       |   +---mention
|   |       |   |       label.go
|   |       |   |
|   |       |   +---status
|   |       |   +---text_type
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           data_model.go
|   |       |   |           dt-type.go
|   |       |   |
|   |       |   +---tokens
|   |       |   |   |   label.go
|   |       |   |   |   README.md
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           data_model.go
|   |       |   |           dt-analyzer.go
|   |       |   |           dt-token.go
|   |       |   |
|   |       |   +---translation
|   |       |   |       label.go
|   |       |   |
|   |       |   \---translation_suggestion
|   |       |           label.go
|   |       |
|   |       +---edges-loop
|   |       |   |   text.go
|   |       |   |   types.go
|   |       |   |
|   |       |   +---anchor_text
|   |       |   |       label.go
|   |       |   |
|   |       |   +---command
|   |       |   |       label.go
|   |       |   |
|   |       |   +---detection-fraud
|   |       |   |       label.go
|   |       |   |
|   |       |   +---detection-spam
|   |       |   |       label.go
|   |       |   |
|   |       |   +---detection-toxicity
|   |       |   |       label.go
|   |       |   |
|   |       |   +---emoticon
|   |       |   |       label.go
|   |       |   |
|   |       |   +---hashtag
|   |       |   |       label.go
|   |       |   |
|   |       |   +---lowercase
|   |       |   |       label.go
|   |       |   |
|   |       |   +---mention
|   |       |   |       label.go
|   |       |   |
|   |       |   +---phrase
|   |       |   |       label.go
|   |       |   |
|   |       |   +---prompt
|   |       |   |       label.go
|   |       |   |       README.md
|   |       |   |
|   |       |   +---query
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           data_model.go
|   |       |   |           dt-precision.go
|   |       |   |           model.go
|   |       |   |
|   |       |   +---spam
|   |       |   |       label.go
|   |       |   |
|   |       |   +---tag
|   |       |   |       label.go
|   |       |   |
|   |       |   +---term
|   |       |   |       label.go
|   |       |   |
|   |       |   +---text
|   |       |   |       label.go
|   |       |   |
|   |       |   +---typo
|   |       |   |       label.go
|   |       |   |
|   |       |   \---word
|   |       |           label.go
|   |       |
|   |       +---edges-shortcut
|   |       |   +---spam_checked
|   |       |   |       label.go
|   |       |   |
|   |       |   +---spam_flaged-rule
|   |       |   |       label.go
|   |       |   |
|   |       |   \---spam_flaged-user
|   |       |           label.go
|   |       |
|   |       +---errors
|   |       |       errors.go
|   |       |       locale.eng.go
|   |       |       locale.per.go
|   |       |
|   |       +---internal
|   |       |   \---matn_____
|   |       |           errors.go
|   |       |           phrase.go
|   |       |           text-index-find.go
|   |       |           text-index-get.go
|   |       |           text-index-set.go
|   |       |           text-index-set_test.go
|   |       |           word-suggestion.go
|   |       |           word.go
|   |       |
|   |       +---protocol
|   |       |       dt-text.go
|   |       |       dt-uuid.go
|   |       |       model.go
|   |       |
|   |       +---rules
|   |       |   +---detection-fraud
|   |       |   +---detection-spam
|   |       |   |       label.go
|   |       |   |
|   |       |   +---detection-toxicity
|   |       |   \---GRAMMAR_CHECKED
|   |       \---widgets
|   |           +---text
|   |           |   \---protocol
|   |           |           business-services.go
|   |           |           gui-widget.go
|   |           |           storage.go
|   |           |
|   |           \---text-editor
|   |                   validator.go
|   |
|   +---management
|   |   |   README.md
|   |   |
|   |   +---calendar
|   |   |   +---edges
|   |   |   |   +---reason
|   |   |   |   |       cooking.go
|   |   |   |   |       end-manual.go
|   |   |   |   |       end.go
|   |   |   |   |       enter-manual.go
|   |   |   |   |       enter.go
|   |   |   |   |       event.go
|   |   |   |   |       exit-manual.go
|   |   |   |   |       exit.go
|   |   |   |   |       packaging.go
|   |   |   |   |       start-manual.go
|   |   |   |   |       start.go
|   |   |   |   |
|   |   |   |   \---type
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---department
|   |   |   +---edges
|   |   |   |   |   group-relation-estate.go
|   |   |   |   |
|   |   |   |   +---department
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---recruit
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           business-services.go
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---group
|   |   |   +---edges
|   |   |   |   +---blocked
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---group
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---invite
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---joined
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---membership-term-member_limit
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---membership-term-skill
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---parent
|   |   |   |   |       gui.go
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---request_to_join
|   |   |   |           gui.go
|   |   |   |           label.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       data_model.go
|   |   |   |       dt-uuid.go
|   |   |   |       model.go
|   |   |   |
|   |   |   \---rules
|   |   |       |   task-relation-rule.go
|   |   |       |
|   |   |       +---authorization
|   |   |       |   |   label.go
|   |   |       |   |
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |           dt-access.go
|   |   |       |           dt-policy.go
|   |   |       |           group.go
|   |   |       |
|   |   |       \---invite
|   |   |           |   label.go
|   |   |           |
|   |   |           \---protocol
|   |   |                   consumer.go
|   |   |                   dt-delegate_type.go
|   |   |                   group.go
|   |   |                   time_validity.go
|   |   |                   user-delegate.go
|   |   |
|   |   +---meeting
|   |   |   +---edges
|   |   |   |   +---location
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---meeting
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---organization
|   |   |       calendar-event.go
|   |   |       calendar.go
|   |   |
|   |   +---project
|   |   |       label.go
|   |   |
|   |   +---role
|   |   |   |   README.md
|   |   |   |
|   |   |   +---data
|   |   |   |   +---c level manager
|   |   |   |   \---judge
|   |   |   |           label.go
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   group-relation-group.go
|   |   |   |   |
|   |   |   |   \---role
|   |   |   |           label.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---rules
|   |   |       +---access-control
|   |   |       |   |   app-connection.go
|   |   |       |   |   README.md
|   |   |       |   |
|   |   |       |   +---errors
|   |   |       |   |       errors.go
|   |   |       |   |       locale.eng.go
|   |   |       |   |       locale.per.go
|   |   |       |   |
|   |   |       |   +---internal
|   |   |       |   |       access_control.go
|   |   |       |   |       _____zero_trust.go
|   |   |       |   |
|   |   |       |   \---protocol
|   |   |       |           authorization.go
|   |   |       |           business-services.go
|   |   |       |
|   |   |       +---salary-earth-hourly
|   |   |       |   |   label.go
|   |   |       |   |
|   |   |       |   \---protocol
|   |   |       |           base-hourly.go
|   |   |       |
|   |   |       +---salary-earth-weekly
|   |   |       |   |   label.go
|   |   |       |   |
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |           storage.go
|   |   |       |
|   |   |       \---salary-floating
|   |   |           |   label.go
|   |   |           |
|   |   |           \---protocol
|   |   |                   coefficients.go
|   |   |
|   |   +---shift
|   |   |   |   label.go
|   |   |   |
|   |   |   +---edges
|   |   |   |       shift.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---staff
|   |   |   +---analytics
|   |   |   |   \---staff-attendance-utc_day
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               storage.go
|   |   |   |
|   |   |   +---edges
|   |   |   |       staff-attendance.go
|   |   |   |       staff-relation-estate.go
|   |   |   |       staff-relation-group.go
|   |   |   |       staff-relation-staff.go
|   |   |   |       staff-status.go
|   |   |   |       staff.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---task
|   |   |   |   README.md
|   |   |   |
|   |   |   +---analytics
|   |   |   |   \---task-utc_day
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               storage.go
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   task-relation-content.go
|   |   |   |   |   task-relation-estate.go
|   |   |   |   |   task-relation-invoice.go
|   |   |   |   |   task-relation-product.go
|   |   |   |   |   task-relation-production.go
|   |   |   |   |   task-relation-skill.go
|   |   |   |   |   task-relation-task.go
|   |   |   |   |
|   |   |   |   +---advertisement
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---campaign
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---marketing
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---process_based
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---repetitive
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---settlement-reference
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---status
|   |   |   |   |       task-status.go
|   |   |   |   |
|   |   |   |   \---time_based
|   |   |   |           label.go
|   |   |   |
|   |   |   +---edges-loop
|   |   |   |       task-relation-table.go
|   |   |   |       task.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   \---timeline
|   |       |   README.md
|   |       |
|   |       +---analytics
|   |       |   \---timeline
|   |       |       \---protocol
|   |       |               data_model.go
|   |       |
|   |       +---edges
|   |       |   |   group-relation-group.go
|   |       |   |   user-relation-group.go
|   |       |   |
|   |       |   +---blocked-text
|   |       |   |       label.go
|   |       |   |
|   |       |   +---event
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           dt-reason.go
|   |       |   |           service-set_event.go
|   |       |   |
|   |       |   +---limit_event_per_user
|   |       |   |       label.go
|   |       |   |
|   |       |   +---limit_max_event
|   |       |   |       label.go
|   |       |   |
|   |       |   +---mute
|   |       |   |       label.go
|   |       |   |
|   |       |   +---pin
|   |       |   |       label.go
|   |       |   |
|   |       |   +---read_until
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           data_model.go
|   |       |   |
|   |       |   \---timeline
|   |       |           label.go
|   |       |
|   |       \---protocol
|   |               dt-uuid.go
|   |
|   +---rights
|   |   |   README.md
|   |   |
|   |   +---case
|   |   |   |   Readme.MD
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   case-relation-case.go
|   |   |   |   |   case-relation-service.go
|   |   |   |   |   case-relation-user.go
|   |   |   |   |   case.go
|   |   |   |   |
|   |   |   |   +---illegal
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---kidnap
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---settlement_for
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---stolen
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---contract
|   |   |   +---analytics
|   |   |   |   \---contract-analytic
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---code
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---financial
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---form_relation
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---legal_action
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---settlement_by
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---signature
|   |   |   |   +---status
|   |   |   |   |       canceled.go
|   |   |   |   |       done.go
|   |   |   |   |       negotiation.go
|   |   |   |   |       signed-partly.go
|   |   |   |   |       signed.go
|   |   |   |   |
|   |   |   |   +---terms
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-data.go
|   |   |   |   |
|   |   |   |   +---user-arbitrator
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-expert
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-side-fifth
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-side-first
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-side-fourth
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-side-second
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-side-third
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---user-side-third copy
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---user-side-fourth
|   |   |   |   |           label.go
|   |   |   |   |
|   |   |   |   \---user-witness
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---delegate
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---attorney
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---representative
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           data_model.go
|   |   |           dt-user-given_delegate.go
|   |   |           dt-user-gotten_delegate.go
|   |   |           storage.go
|   |   |
|   |   +---law
|   |   |   +---edges
|   |   |   |   |   aggregation.go
|   |   |   |   |   law-status.go
|   |   |   |   |
|   |   |   |   +---code
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---computer_code
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---executive_guarantee
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---explanation
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---goal
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---vote-abstention
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---vote-agree
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---vote-disagree
|   |   |   |           label.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---widgets
|   |   |       \---election
|   |   |               README.md
|   |   |
|   |   \---ownership
|   |       |   README.md
|   |       |
|   |       +---edges
|   |       |   +---belongs_to-module
|   |       |   |       label.go
|   |       |   |
|   |       |   +---belongs_to-org
|   |       |   |       label.go
|   |       |   |
|   |       |   +---confirmation
|   |       |   |       label.go
|   |       |   |
|   |       |   +---creator
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   \---creator
|   |       |   |           label.go
|   |       |   |
|   |       |   +---delegate
|   |       |   +---heir
|   |       |   |       label.go
|   |       |   |
|   |       |   +---issuer
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           dt-uuid.go
|   |       |   |
|   |       |   +---owner
|   |       |   |   |   label.go
|   |       |   |   |
|   |       |   |   \---protocol
|   |       |   |           dt-uuid.go
|   |       |   |
|   |       |   +---participant
|   |       |   |       label.go
|   |       |   |
|   |       |   \---reserved
|   |       |           label.go
|   |       |
|   |       +---edges-loop
|   |       |   |   content-relation-user.go
|   |       |   |   task-relation-group.go
|   |       |   |   task-relation-staff.go
|   |       |   |   task-relation-user.go
|   |       |   |
|   |       |   \---assigner
|   |       |           label.go
|   |       |
|   |       \---protocol
|   |               dt-uuid.go
|   |
|   \---storage
|       |   README.md
|       |
|       +---analytic
|       |       service-analytic-query-sdk.go
|       |       service-analytic-query.go
|       |
|       +---directory
|       +---file
|       +---graph
|       |   |   README.md
|       |   |
|       |   +---fields
|       |   |   +---relation-desirability
|       |   |   |   \---protocol
|       |   |   \---relation-priority
|       |   |       \---protocol
|       |   \---protocol
|       |           business-services.go
|       |           data_model.go
|       |           dt-relation-desirability.go
|       |           dt-relation-priority.go
|       |           gui-widget.go
|       |           ss-event_target.go
|       |           storage.go
|       |           storage1.go
|       |
|       +---key_value
|       |   |   README.md
|       |   |
|       |   \---protocol
|       |           dt-key.go
|       |           dt-value.go
|       |           model.go
|       |
|       +---record
|       \---sql
+---modules-plugable
|   +---economics
|   |   |   account.go
|   |   |
|   |   +---account_relationship
|   |   |   +---edges
|   |   |   |   +---limit-transfer
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   +---main_account-give
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   \---main_account-take
|   |   |   |           label.go
|   |   |   |
|   |   |   \---edges-loop
|   |   |       \---limit-amount
|   |   |           |   label.go
|   |   |           |
|   |   |           \---protocol
|   |   |                   transfer-amount.go
|   |   |
|   |   +---analytics
|   |   |   +---break_even_point
|   |   |   +---burn_rate
|   |   |   +---churn_rate
|   |   |   +---customer_acquisition_cost
|   |   |   +---financial-analysis
|   |   |   |   \---protocol
|   |   |   |           data_model.go
|   |   |   |
|   |   |   +---pair_amount
|   |   |   |   \---protocol
|   |   |   |           data_model.go
|   |   |   |           storage.go
|   |   |   |
|   |   |   +---pair_amount-utc-minute
|   |   |   |   \---protocol
|   |   |   |           data_model.go
|   |   |   |           storage.go
|   |   |   |
|   |   |   +---profit_margin
|   |   |   +---return_on_investment
|   |   |   +---sales_cycle_length
|   |   |   +---user-credit
|   |   |   |   \---protocol
|   |   |   |           data_model.go
|   |   |   |           storage.go
|   |   |   |
|   |   |   +---user-credit_debt
|   |   |   |   \---protocol
|   |   |   |           data_model.go
|   |   |   |           storage.go
|   |   |   |
|   |   |   +---user-financial_risk
|   |   |   |   \---protocol
|   |   |   |           data_model.go
|   |   |   |           storage.go
|   |   |   |
|   |   |   +---user-financial_score
|   |   |   |   \---protocol
|   |   |   |           data_model.go
|   |   |   |           storage.go
|   |   |   |
|   |   |   \---user_lifetime_value
|   |   +---analytics-product
|   |   +---batch
|   |   |   +---analytics
|   |   |   |   \---product-supply-inventory
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---accounting
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---batch
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---budget_by
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---cost
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---exist
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---price-settlement
|   |   |   |           label.go
|   |   |   |
|   |   |   +---protocol
|   |   |   |       dt-uuid.go
|   |   |   |
|   |   |   \---rules
|   |   |       \---inventory
|   |   |           |   label.go
|   |   |           |
|   |   |           \---protocol
|   |   |                   inventory-notify.go
|   |   |
|   |   +---brand
|   |   |   |   label.go
|   |   |   |
|   |   |   +---edges
|   |   |   |   \---logo
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---budget
|   |   |   +---edges
|   |   |   |   |   label.go
|   |   |   |   |   transaction-relation-user.go
|   |   |   |   |
|   |   |   |   +---budget
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---nominal
|   |   |   |           label.go
|   |   |   |
|   |   |   +---edges-loop
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---card
|   |   |   +---edges
|   |   |   |   +---authorize_by_card
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---limit_authorize_by_card
|   |   |   |           label.go
|   |   |   |
|   |   |   \---edges-loop
|   |   +---cash
|   |   |   +---edges
|   |   |   |   \---limit-cash
|   |   |   |       |   label.go
|   |   |   |       |
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   +---edges-loop
|   |   |   |   \---cash_account
|   |   |   |           init.go
|   |   |   |           README.md
|   |   |   |
|   |   |   \---edges-shortcut
|   |   |       \---cash_transaction
|   |   |               init.go
|   |   |               README.md
|   |   |
|   |   +---credit
|   |   |   +---edges
|   |   |   \---edges-loop
|   |   |       \---credit_account
|   |   |               label.go
|   |   |
|   |   +---distribution
|   |   |   +---edges
|   |   |   |   +---distribute
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---distribution
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---reject
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---split
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---void
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---finance
|   |   |       README.md
|   |   |
|   |   +---fraud_detection
|   |   |   +---edges
|   |   |   |   +---fraud
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---suspicious
|   |   |   |           label.go
|   |   |   |
|   |   |   \---edges-loop
|   |   |       +---account-score
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |
|   |   |       \---score-risk-assessment-factors
|   |   +---good
|   |   |   +---edges
|   |   |   |   +---best_before
|   |   |   |   |   |   label.go
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           service-set.go
|   |   |   |   |
|   |   |   |   +---branch
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   +---material
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |
|   |   |   |   \---reserve-quantity
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               storage.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---insurance-social
|   |   +---matching_system
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---deal
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---trade
|   |   |   |       |   init.go
|   |   |   |       |   README.md
|   |   |   |       |
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               dt-type.go
|   |   |   |
|   |   |   +---edges-loop
|   |   |   |   +---all_or_none
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   \---instant_withdrawal
|   |   |   |           init.go
|   |   |   |           README.md
|   |   |   |
|   |   |   \---edges-shortcut
|   |   |       +---account-by
|   |   |       |   |   init.go
|   |   |       |   |   README.md
|   |   |       |   |
|   |   |       |   \---protocol
|   |   |       |           data_model.go
|   |   |       |
|   |   |       +---exchange
|   |   |       |       init.go
|   |   |       |       README.md
|   |   |       |
|   |   |       \---fill_or_kill
|   |   |               init.go
|   |   |               README.md
|   |   |
|   |   +---money
|   |   |   +---errors
|   |   |   |       errors.go
|   |   |   |       locale.eng.go
|   |   |   |       locale.per.go
|   |   |   |
|   |   |   +---internal
|   |   |   |       amount.go
|   |   |   |       amount_test.go
|   |   |   |       price.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-money-amout.go
|   |   |           money.go
|   |   |
|   |   +---payroll
|   |   |   +---edges
|   |   |   \---edges-shortcut
|   |   |       \---salary
|   |   |               init.go
|   |   |               README.md
|   |   |
|   |   +---pos
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   |   pos-relation-estate.go
|   |   |   |   |   pos-relation-financial-account.go
|   |   |   |   |   pos-relation-group.go
|   |   |   |   |   pos-relation-staff.go
|   |   |   |   |   pos-status.go
|   |   |   |   |
|   |   |   |   +---page-print_template-customer
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---page-print_template-kitchen
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---page-tv_template-customer
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---price-settlement
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---product-regular
|   |   |   |       |   label.go
|   |   |   |       |
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---production
|   |   |   +---edges
|   |   |   |   |   dt-status.go
|   |   |   |   |
|   |   |   |   +---manufacture
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   +---produce
|   |   |   |   |       label.go
|   |   |   |   |
|   |   |   |   \---production
|   |   |   |           label.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |
|   |   +---products
|   |   |   +---label-commodity
|   |   |   |       label.go
|   |   |   |
|   |   |   +---label-product_final
|   |   |   |       label.go
|   |   |   |
|   |   |   \---label-product_intermediate
|   |   |           label.go
|   |   |
|   |   +---restriction
|   |   |   +---edges
|   |   |   |   +---released_by
|   |   |   |   |       label.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   \---restricted_rule
|   |   |   |           label.go
|   |   |   |           README.md
|   |   |   |
|   |   |   \---edges-shortcut
|   |   |       +---restricted_account
|   |   |       |       label.go
|   |   |       |       README.md
|   |   |       |
|   |   |       +---restricted_user
|   |   |       |       label.go
|   |   |       |       README.md
|   |   |       |
|   |   |       \---restriction_cause
|   |   |               label.go
|   |   |               README.md
|   |   |
|   |   +---securities
|   |   |   +---edges
|   |   |   |   +---securities-for
|   |   |   |   |   |   label.go
|   |   |   |   |   |   READAME.md
|   |   |   |   |   |
|   |   |   |   |   \---protocol
|   |   |   |   |           dt-uuid.go
|   |   |   |   |
|   |   |   |   \---shareholder
|   |   |   |           label.go
|   |   |   |
|   |   |   \---edges-loop
|   |   +---service
|   |   |   +---edges
|   |   |   |   |   product-relation-estate.go
|   |   |   |   |
|   |   |   |   +---multiple-use
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---number
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   +---seat
|   |   |   |   |   \---protocol
|   |   |   |   |           data_model.go
|   |   |   |   |           dt-type.go
|   |   |   |   |           storage.go
|   |   |   |   |
|   |   |   |   \---timing-interval
|   |   |   |       \---protocol
|   |   |   |               data_model.go
|   |   |   |               storage.go
|   |   |   |
|   |   |   \---protocol
|   |   |           dt-uuid.go
|   |   |           model.go
|   |   |
|   |   +---settlement_system
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |   +---endorsement
|   |   |   |   |       init.go
|   |   |   |   |       README.md
|   |   |   |   |
|   |   |   |   \---guarantor
|   |   |   |           init.go
|   |   |   |           README.md
|   |   |   |
|   |   |   \---services
|   |   |       \---endorsement
|   |   +---tax
|   |   +---vat
|   |   |   |   product.go
|   |   |   |   README.md
|   |   |   |
|   |   |   +---edges
|   |   |   |       tax-relation-budget.go
|   |   |   |       tax-relation-financial_account.go
|   |   |   |       tax-relation-product.go
|   |   |   |       tax-relation-rule.go
|   |   |   |       tax.go
|   |   |   |
|   |   |   \---protocol
|   |   |       \---protocol
|   |   |               data_model.go
|   |   |               dt-uuid.go
|   |   |               invoice.go
|   |   |               product.go
|   |   |               value.go
|   |   |
|   |   \---wage
|   |       \---protocol
|   |               data_model.go
|   |
|   +---knowledge
|   \---uri
|       |   README.md
|       |
|       +---account-internal-id
|       |   \---protocol
|       |           business-services.go
|       |           data_model.go
|       |           dt-id.go
|       |           storage.go
|       |
|       +---address
|       |   |   label.go
|       |   |   README.md
|       |   |
|       |   +---edges
|       |   |   +---address-billing
|       |   |   |       label.go
|       |   |   |
|       |   |   +---address-home
|       |   |   |       label.go
|       |   |   |
|       |   |   \---address-work
|       |   |           label.go
|       |   |
|       |   \---protocol
|       |           data_model.go
|       |           dt-uuid.go
|       |
|       +---bio
|       |       label.go
|       |
|       +---government-iran-nin
|       |       user-id.go
|       |
|       +---government-iran-tin
|       +---government-passport-number
|       |       README.md
|       |
|       +---gtin
|       +---iban
|       |   |   label.go
|       |   |
|       |   \---protocol
|       |           business-services.go
|       |           data_model.go
|       |           iban.go
|       |           storage.go
|       |
|       +---imei
|       |       label.go
|       |       README.md
|       |
|       +---internet-domain-name
|       |   \---protocol
|       |           business-services.go
|       |           data_model.go
|       |           dt-ap.go
|       |           dt-name.go
|       |           dt-status.go
|       |           storage.go
|       |
|       +---isbn
|       |       label.go
|       |
|       +---iso-3166
|       |       location.go
|       |
|       +---iso-4217
|       |       currency.go
|       |
|       +---iso-7812
|       |   |   label.go
|       |   |
|       |   +---bank
|       |   |       card.go
|       |   |       iran.go
|       |   |
|       |   \---protocol
|       |           business-services.go
|       |           card.go
|       |           data_model.go
|       |           dt-uuid.go
|       |           storage.go
|       |
|       +---name-display
|       |       label.go
|       |
|       +---name-first
|       |       label.go
|       |
|       +---name-given
|       |       label.go
|       |
|       +---name-last
|       |       label.go
|       |
|       +---name-middle
|       |       label.go
|       |
|       +---name-nick
|       |       label.go
|       |
|       +---name-sur
|       |       label.go
|       |
|       +---net-address
|       |       label.go
|       |       README.md
|       |
|       +---number-itu
|       |   |   label.go
|       |   |
|       |   \---protocol
|       |           business-services.go
|       |           data_model.go
|       |           dt-number.go
|       |           storage.go
|       |
|       +---number-lot
|       |   |   README.md
|       |   |
|       |   \---protocol
|       |           dt-uuid.go
|       |
|       +---number-serial
|       |   \---protocol
|       |           data_model.go
|       |
|       +---postal_code
|       |   |   label.go
|       |   |   README.md
|       |   |
|       |   +---edges
|       |   |   \---zip_code
|       |   |           label.go
|       |   |           README.md
|       |   |
|       |   \---protocol
|       |           dt-uuid.go
|       |
|       +---shaparak-hex
|       |   |   label.go
|       |   |
|       |   \---protocol
|       |           data_model.go
|       |           dt-card-hex.go
|       |           storage.go
|       |
|       +---staff-id
|       |   \---protocol
|       |           data_model.go
|       |           storage.go
|       |
|       +---title
|       |       label.go
|       |
|       +---uri-shortener
|       |   |   label.go
|       |   |
|       |   \---protocol
|       |           data_model.go
|       |           dt-id.go
|       |
|       \---username
|           |   label.go
|           |
|           +---errors
|           |       errors.go
|           |
|           +---internal
|           |       validator.go
|           |
|           +---protocol
|           |       service-register.go
|           |
|           \---widget
|               \---protocol
|                       business-services.go
|                       data_model.go
|                       dt-status.go
|                       dt-username.go
|                       storage.go
|
+---____Chats
|       Graph-Modeling-for-User-Relationship-Queries.md
|       مدل_سازی-چک-در-نظام-مالی.md
|
+---____main
|       init-cmd.go
|       init-gui.go
|       init-server-cloud.go
|       init-server-dsl.go
|       init-server-edge.go
|       init-server.go
|       init_module.go
|       install.sh
|       main.go
|
\---____modules
    |   group.go
    |   init copy.go
    |   product-min-slice-to-buy.txt
    |   question-relation-question.go
    |   quiddity-complement.go
    |   quiddity-substitute.go
    |   staff-attendance.go
    |   staff-shift-preference.go
    |   staff-timing-utc.go
    |   user-analytic.go
    |   user-delegate-analytical.go
    |
    +---asset
    |       data-credit.go
    |
    +---captcha
    |   +---internal
    |   |   \---captcha
    |   |           draw.go
    |   |           errors.go
    |   |           init.go
    |   |           locale.eng.go
    |   |           locale.per.go
    |   |           phrase.go
    |   |           phrase_test.go
    |   |           select-object.go
    |   |           status.go
    |   |
    |   +---protocol
    |   \---services
    |           errors.go
    |           init.go
    |           service-get-new-phrase.go
    |           service-get-phrase-audio.go
    |           service-init.go
    |           service-solve-phrase.go
    |
    +---categories
    |   +---internal
    |   +---pages
    |   |       categories.css
    |   |       categories.html
    |   |       categories.js
    |   |
    |   +---protocol
    |   +---services
    |   +---storage
    |   \---widgets
    +---category
    |   \---pages
    |           category.css
    |           category.html
    |           category.js
    |
    +---comment-template
    |   \---protocol
    |           data_model.go
    |
    +---esteghrar
    |       distribution.go
    |       init.go
    |
    +---exchange
    |       modify-foreign-exchange.go
    |       register-foreign-exchange.go
    |       service-exchange.go
    |
    +---financial-account
    |   \---protocol
    |           service-storage-save.go
    |
    +---financial-account-card
    |       service-announce-account-owner.go
    |       storage.go
    |
    +---financial-transaction
    |   +---internal
    |   |   \---storage
    |   |           ganjine.go
    |   |
    |   +---pages
    |   |       transaction.css
    |   |       transaction.html
    |   |       transaction.js
    |   |
    |   \---services
    |           errors.go
    |           service-find-transactions-by-day.go
    |           service-get-transaction.go
    |           service-get-user-balance.go
    |           service-get.go
    |           service-register.go
    |           service-transfer-to-other-user.go
    |           service-transfer.go
    |
    +---financial-transactions
    |   \---pages
    |           transactions.css
    |           transactions.html
    |           transactions.js
    |
    +---fixed-camera
    |       README.md
    |       receive-camera-data.go
    |
    +---group
    |       change-group.go
    |       delete-group.go
    |       get-org-group.go
    |       get-org-groups.go
    |       register-new-group.go
    |
    +---group-user-access-control
    |   +---protocol
    |   |       group-user-access-control.go
    |   |
    |   \---services
    +---group-user-display-name
    |   \---protocol
    |           group-user-display-name.go
    |
    +---health-directive
    |   \---protocol
    |           health-directive.go
    |
    +---invoice
    |   |   buy-new-product.go
    |   |   product-order.go
    |   |   register-product-invoice.go
    |   |   service-approve-invoice.go
    |   |   service-enounce-approve-invoice.go
    |   |   service-receive-invoice-approve.go
    |   |   service-receive-invoice-detail.go
    |   |   service-send-invoice-detail.go
    |   |   storage.go
    |   |
    |   \---pages
    |           invoice.css
    |           invoice.html
    |           invoice.js
    |
    +---invoice-analytical
    |       init.go
    |
    +---invoice-voucher
    |       storage.sql
    |
    +---invoices
    |   \---pages
    |           invoices.css
    |           invoices.html
    |           invoices.js
    |
    +---law-vote
    |       const.go
    |
    +---life-log
    |   +---pages
    |   +---protocol
    |   |       life-log.go
    |   |
    |   +---services
    |   \---widgets
    +---org-contracts
    |   \---pages
    |           contracts.css
    |           contracts.html
    |           contracts.js
    |
    +---org-department
    |   \---pages
    |           department.css
    |           department.html
    |           department.js
    |
    +---org-pos
    |   \---pages
    |           pos.css
    |           pos.html
    |           pos.js
    |
    +---org-salary
    |   \---pages
    |           salary.css
    |           salary.html
    |           salary.js
    |
    +---organization
    |       errors.go
    |       register-org.go
    |       service-block.go
    |       service-change-domain.go
    |       service-close.go
    |       service-get-last-organizations-id.go
    |       service-get.go
    |       service-register.go
    |       service-unblock.go
    |       storage.go
    |
    +---passport
    |       connect-foreign-platform.go
    |       get-cached-data.go
    |       remove-foreign-platform.go
    |       set-foreign-detail-manually.go
    |
    +---person-password
    |   |   init.go
    |   |
    |   +---internal
    |   |   \---storage
    |   |           storage.go
    |   |           storage_test.go
    |   |
    |   +---pages
    |   |       password.css
    |   |       password.html
    |   |       password.js
    |   |
    |   \---services
    |           errors.go
    |           service-block.go
    |           service-change-password.go
    |           service-deactivate.go
    |           service-get-status.go
    |           service-recover-account.go
    |           service-register.go
    |           service-send-otp.go
    |           service-set-otp.go
    |           service-unblock.go
    |
    +---person-position
    |       approve-org-position-by-person.go
    |       change-postion-status.go
    |       get-person-positions.go
    |       register-new-position.go
    |       suggest-position-to-person.go
    |
    +---person-register
    |   \---pages
    |           register.css
    |           register.html
    |           register.js
    |
    +---product
    |   +---pages
    |   |       page.go
    |   |       product.css
    |   |       product.html
    |   |       product.js
    |   |       state.go
    |   |
    |   \---protocol
    +---product-auction
    |       approve-product-auction-by-warehouse.go
    |       find-product-auction-by-distribution-center-id.go
    |       find-product-auction-by-group-id.go
    |       find-product-auction-by-org-id.go
    |       find-product-auction-by-quiddity-id-distribution-center-id.go
    |       find-product-auction-by-quiddity-id-group-id.go
    |       find-product-auction-by-quiddity-id.go
    |       get-product-auction.go
    |       product-sale.go
    |       register-custom-product-auction.go
    |       register-default-product-auction.go
    |       storage.go
    |       update-product-auction.go
    |
    +---product-cost
    |       storage.go
    |
    +---product-inventory
    |       find-product-by-quiddity-id-dc-id.go
    |       find-product-by-quiddity-id-owner-id.go
    |       find-product-quiddities-id-by-dc-id.go
    |       get-product-inventory-dc-quiddity-number.go
    |       get-product.go
    |       product-inventory_init.go
    |       register-product-inventory.go
    |       register-product-invoice_test.go
    |       storage.go
    |       update-product-dc.go
    |       update-product-owner.go
    |
    +---product-price
    |       find-product-price-by-org-id.go
    |       get-product-price.go
    |       register-product-price.go
    |       storage.go
    |       update-product-price.go
    |
    +---products
    |       products.css
    |       products.html
    |       products.js
    |
    +---questionnaire
    |       README.md
    |
    +---quiddity-domain
    |   |   init-server.go
    |   |   module.go
    |   |
    |   +---internal
    |   |   \---storage
    |   |           ganjine.go
    |   |           mediatype.go
    |   |           mysql.go
    |   |           mysql.sql
    |   |           struct.go
    |   |           syllab.go
    |   |           volatile-memory.go
    |   |
    |   +---pages
    |   +---protocol
    |   |       service-get.go
    |   |       service-register.go
    |   |       storage.go
    |   |
    |   \---services
    |       +---get
    |       |       logic.go
    |       |       req.go
    |       |       sdk.go
    |       |       server.go
    |       |       service.go
    |       |
    |       \---register
    |               logic.go
    |               req.go
    |               sdk.go
    |               server.go
    |               service.go
    |
    +---quiddity-status
    |       init.go
    |       service_find-quiddity-by-org-id.go
    |       service_find-quiddity-by-title.go
    |       service_find-quiddity-by-uri.go
    |       service_get-quiddity-languages.go
    |       service_get-quiddity.go
    |       service_register-quiddity-new-language.go
    |       service_register-quiddity.go
    |       service_update-quiddity.go
    |       storage-syllab.go
    |       storage.go
    |       storage_libgo.go
    |       storage_mysql.go
    |       storage_volatile-memory.go
    |
    +---role
    |   +---internal
    |   |   \---storage
    |   |           mysql.go
    |   |           storage.go
    |   |           volatile-memory.go
    |   |
    |   +---pages
    |   |       role.css
    |   |       role.html
    |   |       role.js
    |   |
    |   +---protocol
    |   |       storage.go
    |   |
    |   \---services
    |           get.go
    |
    +---shopping-cart
    |   +---cart
    |   |       cart.css
    |   |       cart.html
    |   |       cart.js
    |   |
    |   +---payment
    |   |       payment.css
    |   |       payment.html
    |   |       payment.js
    |   |
    |   +---shipping
    |   |       shipping.css
    |   |       shipping.html
    |   |       shipping.js
    |   |
    |   \---summary
    |           summary.css
    |           summary.html
    |           summary.js
    |
    +---sms
    |   |   init-gui.go
    |   |   init.go
    |   |   module.go
    |   |
    |   +---internal
    |   |   \---storage
    |   +---pages
    |   +---protocol
    |   +---services
    |   |       get-event-handler.go
    |   |       init.go
    |   |
    |   \---widgets
    +---store
    |   \---pages
    |           store.css
    |           store.html
    |           store.js
    |
    +---task
    |   |   init-gui.go
    |   |   init-server.go
    |   |   module.go
    |   |   README.md
    |   |
    |   +---fields
    |   +---internal
    |   |   \---storage
    |   +---pages
    |   +---protocol
    |   +---services
    |   |   +---service1
    |   |   \---service2
    |   \---widgets
    +---user-comment
    |   \---pages
    |           comment.css
    |           comment.html
    |           comment.js
    |
    +---user-display-name
    |       user-display-name.go
    |
    +---user-domain
    |       init.go
    |       status.go
    |
    +---user-name
    |       service_get.go
    |       service_register-req.go
    |       service_register.go
    |       storage.go
    |
    +---user-number
    |   +---internal
    |   |   \---storage
    |   |           storage.go
    |   |
    |   \---services
    |           errors.go
    |           get-active.go
    |           get-status.go
    |           register.go
    |           send-sms-to-users.go
    |
    +---user-picture
    |       get-user-picture.go
    |       set-user-picture.go
    |       storage.go
    |
    +---user-request
    |   +---internal
    |   |   \---storage
    |   |           storage.go
    |   |
    |   \---protocol
    |           doc.go
    |           storage.go
    |           uuid.go
    |
    +---user-request-chain
    |   +---internal
    |   |   \---storage
    |   \---protocol
    |           storage.go
    |
    +---user-request-data
    |   +---internal
    |   |   \---storage
    |   \---protocol
    |           storage.go
    |
    +---user-request-metric
    |   +---internal
    |   |   \---storage
    |   \---protocol
    |           storage.go
    |
    +---user-role
    |   \---pages
    |           role.css
    |           role.html
    |           role.js
    |
    +---voucher
    |   |   storage_mysql.sql
    |   |   storage_volatile-memory.go
    |   |
    |   \---pages
    |           voucher.css
    |           voucher.html
    |           voucher.js
    |
    +---vouchers
    |   \---pages
    |           vouchers.css
    |           vouchers.html
    |           vouchers.js
    |
    +---wiki
    |       get-wiki-record-ids.go
    |       get-wiki-record.go
    |       register-wiki-record.go
    |
    \---_test
        |   errors.go
        |   organization-authentication-upgrade.go
        |   user-app-connection.go
        |   user-app-connection_test.go
        |
        \---services
                change-product-owner.go
                delegate-order-new-product.go
                errors.go
                get-article..go
                get-immobile-location.go
                get-live-mobile-location.go
                get-mobile-location.go
                get-org-connection.go
                get-products.go
                register-person-connection.go
                register-product-auction.go
                reject-product.go
                set-immobile-location.go
                set-mobile-location.go
                set-product-distribution-center.go
                set-product-status.go
                set-transaction-tags-comment.go
                user-other-app-cache.go
                verify-user.go
```