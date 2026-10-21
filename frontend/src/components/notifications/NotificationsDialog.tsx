import { Bell, Mail } from "lucide-react";
import { Loading } from "../common/Loading";
import { Modal } from "../../components/common/Modal";
import type { MarketplaceState } from "../../hooks/useMarketplace";
import { notificationService } from "../../services/marketplace";
import { date } from "../../utils/presentation";
export function NotificationsDialog({
  auth,
  setDashboard,
  setNotificationsOpen,
  notifications,
  notificationsLoading,
  notificationsError,
  setNotificationsReload,
  setNotifications,
  setToast,
}: Pick<
  MarketplaceState,
  | "auth"
  | "setDashboard"
  | "setNotificationsOpen"
  | "notificationsLoading"
  | "notificationsError"
  | "setNotificationsReload"
  | "notifications"
  | "setNotifications"
  | "setToast"
>) {
  return (
    <Modal title="Notifications" onClose={() => setNotificationsOpen(false)}>
      <div className="modal-body">
        {notificationsLoading ? (
          <Loading />
        ) : notificationsError ? (
          <div className="empty-state compact">
            <p role="alert" className="form-error">
              {notificationsError}
            </p>
            <button
              className="button button-outline"
              onClick={() => setNotificationsReload((value) => value + 1)}
            >
              Retry notifications
            </button>
          </div>
        ) : notifications.length === 0 ? (
          <div className="empty-state compact">
            <Bell size={30} />
            <h3>You’re all caught up</h3>
            <p>New service inquiries will appear here.</p>
          </div>
        ) : (
          notifications.map((n) => (
            <button
              className={`notification-row ${n.read ? "" : "unread"}`}
              key={n.id}
              onClick={async () => {
                try {
                  await notificationService.read(auth!, n.id);
                  setNotifications(
                    notifications.map((x) =>
                      x.id === n.id ? { ...x, read: true } : x,
                    ),
                  );
                  setNotificationsOpen(false);
                  setDashboard(true);
                } catch (e) {
                  setToast((e as Error).message);
                }
              }}
            >
              <span className="notification-symbol">
                <Mail size={19} />
              </span>
              <span>
                <strong>{n.message}</strong>
                <small>{date(n.createdAt)}</small>
              </span>
              {!n.read && <span className="unread-dot" />}
            </button>
          ))
        )}
      </div>
    </Modal>
  );
}
