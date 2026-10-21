import { spawn } from 'node:child_process';
const service = process.argv[2];
if (!['identity', 'catalog', 'inquiries', 'notifications'].includes(service)) {
  throw new Error('Expected service name');
}
const outDir = `dist-dev/${service}`;
const compiler = 'node_modules/typescript/bin/tsc';
const build = spawn(process.execPath, [compiler, '--outDir', outDir], { stdio: 'inherit' });
const built = await new Promise((resolve) => build.on('exit', resolve));
if (built !== 0) process.exit(Number(built ?? 1));
const children = [
  spawn(process.execPath, [compiler, '--watch', '--outDir', outDir, '--preserveWatchOutput'], {
    stdio: 'inherit',
  }),
  spawn(
    process.execPath,
    [
      '--watch',
      ...(process.env.INSPECT_PORT ? [`--inspect=127.0.0.1:${process.env.INSPECT_PORT}`] : []),
      `${outDir}/main.js`,
    ],
    {
      env: { ...process.env, SERVICE: service },
      stdio: 'inherit',
    },
  ),
];
let stopping = false;
function stop() {
  if (stopping) return;
  stopping = true;
  for (const child of children) child.kill('SIGTERM');
}
process.on('SIGINT', stop);
process.on('SIGTERM', stop);
for (const child of children)
  child.on('exit', (code) => {
    if (!stopping) {
      process.exitCode = code || 1;
      stop();
    }
  });
