import { X } from "lucide-react";
import type React from "react";
import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";
const openDialogs: { id: symbol; backdrop: HTMLElement }[] = [];
const backgroundState = new Map<
  HTMLElement,
  { inert: boolean; hidden: string | null }
>();
function isolateTopDialog() {
  const top = openDialogs.at(-1)?.backdrop;
  if (!top) {
    for (const [element, state] of backgroundState) {
      element.inert = state.inert;
      if (state.hidden === null) element.removeAttribute("aria-hidden");
      else element.setAttribute("aria-hidden", state.hidden);
    }
    backgroundState.clear();
    return;
  }
  for (const child of Array.from(document.body.children)) {
    if (!(child instanceof HTMLElement)) continue;
    if (!backgroundState.has(child))
      backgroundState.set(child, {
        inert: child.inert,
        hidden: child.getAttribute("aria-hidden"),
      });
    child.inert = child !== top;
    if (child === top) child.removeAttribute("aria-hidden");
    else child.setAttribute("aria-hidden", "true");
  }
}
let originalOverflow = "";
export function Modal({
  title,
  children,
  onClose,
  wide = false,
}: {
  title: string;
  children: React.ReactNode;
  onClose: () => void;
  wide?: boolean;
}) {
  const dialogRef = useRef<HTMLElement>(null);
  const backdropRef = useRef<HTMLDivElement>(null);
  const onCloseRef = useRef(onClose);
  useEffect(() => {
    onCloseRef.current = onClose;
  }, [onClose]);
  useEffect(() => {
    const id = Symbol("dialog");
    if (openDialogs.length === 0)
      originalOverflow = document.body.style.overflow;
    if (!backdropRef.current) return;
    openDialogs.push({ id, backdrop: backdropRef.current });
    isolateTopDialog();
    const previous = document.activeElement as HTMLElement | null;
    const focusable = () =>
      Array.from(
        dialogRef.current?.querySelectorAll<HTMLElement>(
          'button:not([disabled]),a[href],input,select,textarea,[tabindex="0"]',
        ) || [],
      );
    focusable()[0]?.focus();
    const h = (e: KeyboardEvent) => {
      if (openDialogs.at(-1)?.id !== id) return;
      if (e.key === "Escape") onCloseRef.current();
      if (e.key === "Tab") {
        const els = focusable();
        const first = els[0],
          last = els[els.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last?.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first?.focus();
        }
      }
    };
    document.addEventListener("keydown", h);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", h);
      openDialogs.splice(
        openDialogs.findIndex((dialog) => dialog.id === id),
        1,
      );
      isolateTopDialog();
      if (openDialogs.length === 0)
        document.body.style.overflow = originalOverflow;
      if (previous?.isConnected) previous.focus();
    };
  }, []);
  return createPortal(
    <div
      ref={backdropRef}
      className="modal-backdrop"
      role="presentation"
      onMouseDown={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <section
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className={`modal ${wide ? "modal-wide" : ""}`}
      >
        <div className="modal-heading">
          <h2>{title}</h2>
          <button
            className="icon-button"
            aria-label="Close dialog"
            onClick={onClose}
          >
            <X size={21} />
          </button>
        </div>
        {children}
      </section>
    </div>,
    document.body,
  );
}
