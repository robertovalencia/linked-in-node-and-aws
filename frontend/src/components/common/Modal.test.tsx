import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it, vi } from "vitest";
import { Modal } from "./Modal";
it("only dismisses the topmost dialog and restores scrolling after all dialogs close", async () => {
  const first = vi.fn();
  const second = vi.fn();
  const user = userEvent.setup();
  document.body.style.overflow = "auto";
  const { rerender, unmount } = render(
    <>
      <Modal title="Profile" onClose={first}>
        <button>Contact</button>
      </Modal>
      <Modal title="Sign in" onClose={second}>
        <input aria-label="Email" />
      </Modal>
    </>,
  );
  await user.keyboard("{Escape}");
  expect(second).toHaveBeenCalledOnce();
  expect(first).not.toHaveBeenCalled();
  expect(document.body.style.overflow).toBe("hidden");
  rerender(
    <Modal title="Profile" onClose={first}>
      <button>Contact</button>
    </Modal>,
  );
  expect(screen.getByRole("dialog", { name: "Profile" })).toBeInTheDocument();
  expect(document.body.style.overflow).toBe("hidden");
  unmount();
  expect(document.body.style.overflow).toBe("auto");
});

it("isolates background and lower dialogs from keyboard and accessibility navigation", async () => {
  const user = userEvent.setup();
  const { rerender, container, unmount } = render(
    <>
      <button>Background action</button>
      <Modal title="Profile" onClose={vi.fn()}>
        <button>Contact</button>
      </Modal>
      <Modal title="Sign in" onClose={vi.fn()}>
        <input aria-label="Email" />
        <button>Submit</button>
      </Modal>
    </>,
  );
  const top = screen.getByRole("dialog", { name: "Sign in" });
  expect(container.inert).toBe(true);
  expect(container).toHaveAttribute("aria-hidden", "true");
  expect(
    screen.queryByRole("dialog", { name: "Profile" }),
  ).not.toBeInTheDocument();
  expect(
    screen.queryByRole("button", { name: "Background action" }),
  ).not.toBeInTheDocument();
  const submit = within(top).getByRole("button", { name: "Submit" });
  submit.focus();
  await user.tab();
  expect(
    within(top).getByRole("button", { name: "Close dialog" }),
  ).toHaveFocus();
  await user.tab({ shift: true });
  expect(submit).toHaveFocus();
  rerender(
    <>
      <button>Background action</button>
      <Modal title="Profile" onClose={vi.fn()}>
        <button>Contact</button>
      </Modal>
    </>,
  );
  expect(screen.getByRole("dialog", { name: "Profile" })).toBeVisible();
  expect(container.inert).toBe(true);
  unmount();
  expect(container).not.toHaveAttribute("aria-hidden");
});
